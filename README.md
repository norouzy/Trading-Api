# Trading view
Django rest-framework App 

It's an api for trading websites like tarding view

[Postman link to know how work with apis](https://www.getpostman.com/collections/b664690060c634638fe5)

[Apis deployed on heroku](https://norouzyteam.herokuapp.com
)

[website link](https://trading-app-five.vercel.app/) use VPN to open site:)

# Options
* Trade as a Market or Limit type
* Set Position option (stop loss or take profit)
* User Watch-list
* User wallet
* User paper-tading
* Show real-time market price (Use WebSocket)
* JWT authentication
# images


<details>
  <summary>Home</summary>
  <img src="https://user-images.githubusercontent.com/77892796/179959284-2f4afab2-c3e3-458b-958c-e95a0cc8df94.png" name="image-name">
  <img src="https://user-images.githubusercontent.com/77892796/179959296-7f6329f4-3483-439d-b9ca-c3c4d86e69d8.png" name="image-name">
</details>
<details>
  <summary>Market</summary>
  <img src="https://user-images.githubusercontent.com/77892796/179959299-659259f4-50bc-4405-8ba3-eb30dfe0d469.png" name="image-name">
  <img src="https://user-images.githubusercontent.com/77892796/179961590-7ab072b1-0776-47da-855b-5bd75a72cbfa.png" name="image-name">
  <img src="https://user-images.githubusercontent.com/77892796/179961597-459d0d77-ec4a-43cc-b77f-131c9eb0240a.png" name="image-name">
</details>

<details>
  <summary>Exchange</summary>
  <img src="https://user-images.githubusercontent.com/77892796/179962061-74ce6716-ab8f-4e4f-9f3f-fdd8d717eee7.png" name="image-name">
  <img src="https://user-images.githubusercontent.com/77892796/179962075-ed749c65-1e23-4b34-8e43-211fe91a5995.png" name="image-name">
  <img src="https://user-images.githubusercontent.com/77892796/179962076-4722e482-d98c-42f5-96fc-71af736824c2.png" name="image-name">
  <img src="https://user-images.githubusercontent.com/77892796/179962081-9f3ff443-40a0-4970-a3d6-9c54002fe721.png" name="image-name">
</details>

<details>
  <summary>Panel</summary>
  <img src="https://user-images.githubusercontent.com/77892796/179962603-11868cba-0dd5-4cb7-a667-03a0d5c3e42f.png" name="image-name">
  <img src="https://user-images.githubusercontent.com/77892796/179962614-6ef23f75-9701-494d-8afb-1a91c080a152.png" name="image-name">
  <img src="https://user-images.githubusercontent.com/77892796/179962620-a949a5e9-ddd3-4df2-92ad-fee68f8f7d1f.png" name="image-name">
</details>


# Getting Started
To use this template to start your own project:

clone the project

    git clone https://github.com/norouzy/Trading-Api.git
    
create and start a a virtual environment

    virtualenv env

    source env/bin/activate

Install the project dependencies:

    pip install -r requirements.txt

    
then run

    python manage.py migrate

create admin account

    python manage.py createsuperuser
      
then

    python manage.py makemigrations

to makemigrations for the app

then again run

    python manage.py migrate

to start the development server

    python manage.py runserver

and open localhost:8000 on your browser to view the app.


