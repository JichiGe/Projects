import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import { BrowserRouter } from "react-router-dom";
import WritePage from "../pages/WritePage";


const mockUseAuthToken = jest.fn();

jest.mock("../AuthTokenContext", () => ({
  useAuthToken: () => mockUseAuthToken(),
}));

describe("WritePage Component", () => {
  beforeEach(() => {
    mockUseAuthToken.mockReturnValue({ accessToken: "fake-token" });
  });

  it("should render input for title, description, and categories", () => {
    render(
      <BrowserRouter>
        <WritePage />
      </BrowserRouter>
    );

    expect(screen.getByPlaceholderText("Title")).toBeInTheDocument();

    expect(screen.getByText("Publish")).toBeInTheDocument();

    expect(screen.getByLabelText("Art")).toBeInTheDocument();
    expect(screen.getByLabelText("Science")).toBeInTheDocument();
    expect(screen.getByLabelText("Technology")).toBeInTheDocument();
    expect(screen.getByLabelText("Cinema")).toBeInTheDocument();
    expect(screen.getByLabelText("Design")).toBeInTheDocument();
    expect(screen.getByLabelText("Food")).toBeInTheDocument();
  });

  it("allows typing in the title input", () => {
    render(
      <BrowserRouter>
        <WritePage />
      </BrowserRouter>
    );

    const titleInput = screen.getByPlaceholderText("Title");
    fireEvent.change(titleInput, { target: { value: "New Post Title" } });

    expect(titleInput.value).toBe("New Post Title");
  });
});
