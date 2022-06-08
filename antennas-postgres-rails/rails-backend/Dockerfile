FROM ruby:3.1.2

# Create app directory
WORKDIR /usr/src/app

RUN apt-get update -qq \
&& apt-get install -y nodejs postgresql-client

# Set up gemfile and vendor content, install gems
RUN gem install bundler

COPY Gemfile Gemfile.lock ./
COPY vendor ./vendor
RUN bundle config --local build.sassc --disable-march-tune-native \
  && bundle check || bundle install --without production

# Install rails
RUN bundle install

COPY . ./

# Add a script to be executed every time the container starts.
COPY entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

EXPOSE 5000

CMD ["bundle", "exec", "rails", "s", "-p", "5000",  "-b", "0.0.0.0"]
