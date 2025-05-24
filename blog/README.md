Web address:https://5610-a3.vercel.app/



usage:

    in client folder:
        npm install
        npm start


    in server folder:
        npm install
        npx prisma db push
        npx prisma db seed
        npm start

    to reset the database:
        npx prisma db push --force-reset
        npx prisma db seed


## Client .env

```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_AUTH0_DOMAIN=dev-rmjwrcw1i7sp25hq.us.auth0.com
REACT_APP_AUTH0_CLIENT_ID=XwbFRaqb8hDSizHsRYTvfWN3t1ykiMP8
REACT_APP_AUTH0_AUDIENCE=https://api.blogs

```

## API .env

```
DATABASE_URL=mysql://root:123456@localhost:3306/blogdb
AUTH0_AUDIENCE=https://api.blogs
AUTH0_ISSUER=https://dev-rmjwrcw1i7sp25hq.us.auth0.com/
```
