import React from "react";
import { BrowserRouter as Router } from "react-router-dom";
import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import DetailsPage from "../pages/DetailsPage";
import { useAuth0 } from "@auth0/auth0-react";
import { useAuthToken } from "../AuthTokenContext";

jest.mock("../AuthTokenContext", () => ({
  useAuthToken: () => ({
    accessToken: "mocked_access_token",
  }),
}));

jest.mock("@auth0/auth0-react", () => ({
  useAuth0: () => ({
    user: { sub: "auth0|123" },
    isAuthenticated: true,
  }),
}));

global.fetch = require("jest-fetch-mock");

describe("DetailsPage", () => {
  afterEach(() => {
    fetch.resetMocks();
  });

  it("renders post details correctly", async () => {
    const fakePost = {
      id: 1,
      img: "https://example.com/post.jpg",
      title: "Test Post",
      desc: "<p>Test Description</p>",
      User: {
        userImg: "https://example.com/user.jpg",
        name: "John Doe",
        auth0Id: "auth0|123",
      },
      createdAt: "2020-01-01T00:00:00.000Z",
      Comments: [{ id: 1, text: "Great post!" }],
    };

    fetch.mockResponseOnce(JSON.stringify(fakePost));

    render(
      <Router>
        <DetailsPage />
      </Router>
    );

    await waitFor(() => {
      expect(screen.getByText("Test Post")).toBeInTheDocument();
    });
    expect(screen.getByText("Test Description")).toBeInTheDocument();
    expect(screen.getByText("Great post!")).toBeInTheDocument();
  });
});
