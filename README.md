### [Gaurav Jain](http://www.gauravvjn.com)

#### Install Pelican

```sh
pip install -r requirements.txt

# create local_pelicanconf.py for development settings
cp local_pelicanconf.py.sample local_pelicanconf.py
```

Create .md files in content/ folder

#### Generate Site
From the project root directory, run the pelican command to generate your site:

```sh
pelican content
```

#### Preview site
Open a new terminal session, navigate to your project root directory, and 
run the following command to launch Pelican's web server:
```sh
pelican --listen
```

Preview your site by navigating to http://localhost:8000/ in your browser.
