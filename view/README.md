# Install

`cd` to project's dir and run `npm install`

# Vite builds

[Vite](https://vitejs.dev) is next Generation Frontend Tooling featuring unbundled web-development

## Hot-reloads for development
```
npm run dev
```

## Builds and minifies for production
```
npm run build:vite
```

## Serves recently built app
```
npm run serve:vite
```

# Linting

## Lint
```
npm run lint
```

## Lints and fixes files
```
npm run lint:fix
```

# Docker image
Build the image using:

```
docker build -t view .
```

Run the image "view" and map the container port 80 to the local port 8080
```
docker run -it -p 8080:80 view:latest
```
