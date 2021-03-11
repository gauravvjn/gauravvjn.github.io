---
title: Saving GeoPoints Using Django Form
date: 2020-05-26
category: Django
tags: django, djangoform, geopoint, gis
authors: Gaurav Jain
summary: 
coverimage: /images/saving-geopoints-django-cover.png
---

A while ago I was working on a project where I had a map which was part of a simple form. User can select a point on the map and submit. Form's responsibility was to get the submitted data, validate it and save into database if everything is fine. I was using MySQL with GIS support. During the development I faced a couple of issues that I'd be addressing here and how did I fix them. Let's begin!

Consider the below example

```python
from django.contrib.gis.db import models

class Location(models.Model):
    coordinate = models.PointField(blank=True, null=True)
    # many more fields
```

If you see the Django generated migration file for this model, you will notice that the default value of **srid** parameter is 4326 although we never provided that explicitly in the model definition.  
This is how migration will look like.

```python
operations = [
    migrations.CreateModel(
        name='Location',
        fields=[
            ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('coordinate', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
        ],
    ),
]
```

The default value of **srid** is being propagated from a base class **[BaseSpatialField](https://github.com/django/django/blob/33c365781abbcc1b21a31b31d95d344a174df0d5/django/contrib/gis/db/models/fields.py#L56)**, the PointField has been inherited from. We can always change this value as per requirements but in most cases default value would be sufficient.

Let's try to save some Geo coordinates through the shell. First, we need to import Point class so that we can directly assign the value to the model field. Go ahead and hit the `**python manage.py shell**`

```python
>>> from django.contrib.gis.geos import Point
>>> Point(75.778885, 26.922070)  # Latitude=26.922070 & longitude=75.778885
<Point object at 0x11a282c70>
>>> # save into database
>>> Location.objects.create(coordinate=Point(75.778885, 26.922070))
<Location: Location object (1)>
```

Lets see how it's been stored in the database.

```python
>>> Location.objects.last().coordinate.coords
(75.778885, 26.92207)
```

Looks good. Thats what we saved.

Lets do the same exercise using Django form. Create a **forms.py** file as below

```python
from django.contrib.gis import forms  
# Note: forms is being imported from gis module instead of: `from django import forms`

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('coordinate',)
```

Now, pass the same data to this form and see how it responds.

```python
>>> data = {'coordinate': '75.778885, 26.92207'}
>>> form = LocationForm(data=data)
>>> form
<LocationForm bound=True, valid=Unknown, fields=(coordinate)>
>>>
>>> form.is_valid()  # check if the provided payload is valid 
Error creating geometry from value '75.778885, 26.92207' (String input unrecognized as WKT EWKT, and HEXEWKB.)
```

Oops! We got an error- **Error creating geometry from value '75.778885, 26.92207' (String input unrecognized as WKT EWKT, and HEXEWKB.)**

It seems the data we provided is not in one of the acceptable format. After a bit of searching, I found, I need to provide a proper geometry type with the data.

```python
>>> data = {'coordinate': 'POINT(75.778885 26.92207)'}  # Note that points are separated by a space
>>> form = LocationForm(data=data)
>>> form.is_valid()
True
```

Nice, It worked! Wait... Did it actually? Too soon to celebrate 😏. Let's save this form and verify the data in the database.

```python
>>> form.save()
<Location: Location object (2)>
>>>
>>> # Now Lets see how it was stored in the database
>>> Location.objects.last().coordinate.coords
(0.0006807333060903553, 0.0002418450696118364)
```

Whaaaat?  
![](../images/saving-geopoints-django-1.png)  
This is not what we provided.

What went wrong! Again Django form needs **srid** value explicitly. Let's modify the data a little bit and follow the same steps.

```python
>>> data = {'coordinate': 'SRID=4326;POINT(75.778885 26.92207)'}
>>> form = LocationForm(data=data)
>>> form.is_valid()
True
>>> form.save()
<Location: Location object (3)>
```

Verify the database.

```python
>>> Location.objects.last().coordinate.coords
(75.778885, 26.92207)
>>>
```

Awesome. finally we can see the data that we inserted.

Now the question is how and where should we make this change in the codebase?

We have two options - 
1) We can modify the payload before passing it to the form. But that won't be a good place to do. moreover, we might be using this form in multiple places, in that case, we have to make changes at all those places. That leaves us with 2nd option.

2) We override **\_\_init\_\_** method inside the Form class so that all the logic would be at one place.

```python
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('coordinate',)

    def __init__(self, *args, **kwargs):
        coordinate = kwargs['data'].pop('coordinate', None)
        if coordinate:
            coordinate = coordinate.replace(',', '')  # remove comma, as we need single space between two numbers.
            kwargs['data']['coordinate'] = f'SRID=4326;POINT({coordinate})'

        super(LocationForm, self).__init__(*args, **kwargs)
```

Now we don't need to pass GEOM\_TYPE in the data. we can simply pass the raw point data as we did in the very first step.

```python
>>> data = {'coordinate': '75.778885, 26.92207'}
>>> form = LocationForm(data=data)
>>> form.save()
<Location: Location object (4)>
```

Verify the database.

```python
>>> Location.objects.last().coordinate.coords
(75.778885, 26.92207)
>>>
```

👏👏👏 Sweet!

Additionally, if your business logic required some other conditional checks, then you can override **clean\_<field\_name>** or/and **clean** method, write all the logic there and raise relevant exceptions/validation errors if needed. Also, If you have multiple Point fields in your model, it would make sense to create a method inside the class and reuse that in the **\_\_init\_\_** method.
