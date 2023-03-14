
# Card Tokenizer (Backend)

Card Tokenizer is a app, which takes your card details stores it in encrypted format and generates a token for each card which can used for payments in future making the payment process secure. It also has other features simulated in it like card consumer and card verification.

## Run Locally

Clone the project

```bash
  git clone https://github.com/krish-patel1003/secureCardAPI.git
```

Go to the project directory

```bash
  cd secureCardAPI
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python manage.py makemigrations
  python manage.py migrate
  python manage.py collectstatic
  python manage.py runserver
```

