### [Gaurav Jain](http://www.gauravvjn.com)

#### Install Pelican

```sh
pip install -r requirements.txt
```

Create .md files in content/ folder

#### Generate Site
From the project root directory, run the pelican make command to generate your site:

```sh
make local

# Use make publish to generate site for production
make publish 
```

#### Preview site
Open a new terminal session, navigate to your project root directory, and 
run the following command to launch Pelican's web server:
```sh
pelican --listen
```

Preview your site by navigating to http://localhost:8000/ in your browser.
