![logo_small](https://user-images.githubusercontent.com/64976988/168271445-6a5958af-d534-49cc-8187-4190a12d546b.svg)

Yandex.Lyceum Flask project

Aphorism is the REST API of a new social networking concept or we can call it a podcast platform. Posts can only consist of short captions and a voice message

## Description 📋
 - Each user will have his own profile with gravatar, where you can post, see statistics, change status
 - The feed will consist of posts by people the user is subscribed to. You can "Like" a post as usual
 - Using the search will allow to find new authors 

## Using 🎧
```sh
git clone https://github.com/xDiaym/aphorism.git
```
Move to project's directory
```sh
docker-compose up
```
Check swagger documentation on http://localhost:8000/api/v1/docs

## Testing ✔️
To run the tests, simply do the following in a Linux environment (in Windows it can be WSL)
```sh
tests/test.sh
```
