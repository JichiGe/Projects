// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import ProfilePage from "../pages/ProfilePage";
import { useAuthToken } from "../AuthTokenContext";
jest.mock("../AuthTokenContext");

describe("ProfilePage Component", () => {
  beforeEach(() => {
    useAuthToken.mockReturnValue({ accessToken: "mock-access" });
    global.fetch = jest.fn((url, options) => {
      if (
        url === `${process.env.REACT_APP_API_URL}/profile` &&
        options.method === "GET"
      ) {
        return Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              name: "John Doe",
              email: "JohnDoe.gmail.com",
              picture: "https://example.com/user.jpg",
            }),
        });
      }
    });
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test("renders ProfilePage component with user data", async () => {
    render(<ProfilePage />);
    await waitFor(() => {
      expect(screen.getByText("John Doe")).toBeInTheDocument();
    });

    expect(screen.getByText("JohnDoe.gmail.com")).toBeInTheDocument();
  });
});
