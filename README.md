## Bazaar

Bazaar is a custom E-Commerce website built using [Django](https://www.djangoproject.com/) and [TailwindCSS](https://tailwindcss.com/) that has been integrated and tested with the [Razorpay](https://razorpay.com/docs/api/payments/) payment gateway.  


    


Here is a short walkthrough:

https://github.com/achyuthcodes30/Bazaar/assets/113189939/7babae52-6786-4d09-a426-eca9dc2e52a8


## Features
1. Login/Signup functionalities with menus and pages.
2. Responsive UI and animations built with TailwindCSS.
3. Search functionality that works even with similar keywords.
4. Real-time Cart with update and delete functionalities.
5. Categorisation according to type and seller.
6. Razorpay payment integration.

## Install and run locally
1. Set up a virtual environment.
2. Change directories to your working directory using the ``` cd ``` command.
3. Clone this repository
   ```
   git clone https://github.com/achyuthcodes30/Bazaar.git
   ```
4. Install the requirements
   ```
   pip install -r requirements.txt
   ```
5. Run the server locally
   ```
   python manage.py runserver
   ```

**Note** : To use the payment gateway you will need to add your API key IDs and Secret to the ``` settings.py ``` file after generating them from [RazorpayX](https://x.razorpay.com/):
```
RAZORPAY_KEY_ID= "YOUR_KEY_ID"
RAZORPAY_KEY_SECRET= "YOUR_KEY_SECRET"

```

I have also added the ```db.sqlite3 ``` for some default products and non-sensitive data although it's not recommended (should be in .gitignore).

## Contributing
- Make sure to either fork this repository or create your own branch. (DO NOT PUSH TO MAIN!!)
- Only start working on an issue when you are assigned to it. This helps prevent multiple contributors from working on the same issue at the same time.
- Make a pull request as soon as you are assigned to as issue, this pull request will be used to track your progress on the issue by commits.
- To maintain active collaboration, contributors are expected to have at least one commit to the PR every 30 minutes that indicates progress or an update.
- Maintainers may reach out to contributors if there are no recent updates on an issue.
- If the update is unsatisfactory or if there is no response, the issue may be reassigned to another contributor.

## Maintainer: Achyuth Yogesh Sosale
