import React from "react";
import { createRoot } from "react-dom/client";

import App from "./App";

import { Auth0Provider } from "@auth0/auth0-react";
import { AuthTokenProvider } from "./AuthTokenContext";
import { getConfig } from "./config";


// Please see https://auth0.github.io/auth0-react/interfaces/Auth0ProviderOptions.html
// for a full list of the available properties on the provider
const config = getConfig();

const providerConfig = {
  domain: config.domain,
  clientId: config.clientId,

  authorizationParams: {
    redirect_uri: `${window.location.origin}/verify`,
    ...(config.audience ? { audience: config.audience } : null),
  },
};

const root = createRoot(document.getElementById('root'));
root.render(

  <Auth0Provider
    {...providerConfig}
  >
    <AuthTokenProvider>
      <App />
    </AuthTokenProvider>
  </Auth0Provider>

);