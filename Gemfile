# frozen_string_literal: true

source "https://rubygems.org"

gemspec

# don't change it!
gem "html-proofer", "~> 4.4", group: :test

platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]

# don't change it!
gem "jekyll-archives", path: "assets/jekyll-archives"
gem 'jekyll-compose', group: [:jekyll_plugins]