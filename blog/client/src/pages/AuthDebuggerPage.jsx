import { useAuth0 } from "@auth0/auth0-react";
import { useAuthToken } from "../AuthTokenContext";
import "../style/authDebuggerPage.css";
export default function AuthDebugger() {
  const { user } = useAuth0();
  const { accessToken } = useAuthToken();
  console.log(user);

  return (
    <div >
      <div>
        <p>Access Token:</p>

        <pre>{JSON.stringify(accessToken, null, 2)}</pre>
      </div>
      <div>
        <p>User Info</p>
        <pre>{JSON.stringify(user, null, 2)}</pre>
      </div>
    </div>
  );
}
