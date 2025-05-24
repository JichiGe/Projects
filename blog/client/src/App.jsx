import {
  createBrowserRouter,
  RouterProvider,
  Outlet,
} from "react-router-dom";
import AuthDebuggerPage from "./pages/AuthDebuggerPage";
import DetailsPage from "./pages/DetailsPage";
import HomePage from "./pages/HomePage";
import ProfilePage from "./pages/ProfilePage";
import WritePage from "./pages/WritePage";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import VerifyUser from "./pages/VerifyUser";
import NotFound from "./pages/NotFound";
import {  useAuth0 } from "@auth0/auth0-react";




function RequireAuth({ children }) {
  const { isAuthenticated, isLoading, loginWithRedirect } = useAuth0();

  // If the user is not authenticated, redirect to the home page
  if (!isLoading && !isAuthenticated) {
    loginWithRedirect();
    return null;
  }

  // Otherwise, display the children (the protected page)
  return children;
}


const Layout = () => {
  return (
    <>
      <Navbar />
      <Outlet />
      <Footer />
    </>
  );
}

const router = createBrowserRouter([
  {
    children: [
      {
        path: "/",
        element: <Layout />,
        children: [
          {
            path: "/",
            element: <HomePage />
          },
          {
            path: "/post",
            element:
              <RequireAuth>
                <WritePage />
              </RequireAuth>
          },
          {
            path: "/profile",
            element: (
              <RequireAuth>
                <ProfilePage />
              </RequireAuth>
            ),
          },
          {
            path: "/details/:id",
            element: <DetailsPage />
          },
          {
            path: "/debug",
            element: (
              <RequireAuth>
                <AuthDebuggerPage />
              </RequireAuth>
            ),
          },
          {
            path: "*",
            element: <NotFound />
          },
          {
            path: "/verify",
            element: <VerifyUser />
          }
        ]
      },
    ]
  }
]);

function App() {
  return <div className="app">



    <div className="container">
      <RouterProvider router={router} />
    </div>



  </div>;
}


export default App;
