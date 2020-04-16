### [PyScoop](http://www.pyscoop.com)

### Setting up jekyll for local development and debug

#### Create **Gemfile**
```Gemfile
source 'https://rubygems.org'
gem 'github-pages', group: :jekyll_plugins
```
#### Install jekyll
```sh
brew upgrade ruby
export PATH=/usr/local/bin:$PATH
ruby --version
sudo gem update --system

sudo gem install bundler 
OR try below command
# sudo gem install -n /usr/local/bin bundler
# sudo gem install -n /usr/local/bin nokogiri

bundle install

bundle exec jekyll serve
```
