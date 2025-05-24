import * as dotenv from "dotenv";
dotenv.config();
import express from "express";
import pkg from "@prisma/client";
import morgan from "morgan";
import cors from "cors";
import { auth } from "express-oauth2-jwt-bearer";

// this is a middleware that will validate the access token sent by the client
const requireAuth = auth({
  audience: process.env.AUTH0_AUDIENCE,
  issuerBaseURL: process.env.AUTH0_ISSUER,
  tokenSigningAlg: "RS256",
});

const app = express();

app.use(cors({origin:"*"}));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(morgan("dev"));

const { PrismaClient } = pkg;
const prisma = new PrismaClient();

// Get all blog items
app.get("/blogs", async (req, res) => {
  const category = req.query.cat;
  const blogItems = await prisma.blogItem.findMany({
    where: category ? { category: category } : undefined,
  });
  if (blogItems.length > 0) {
    res.status(200).json(blogItems);
  } else {
    res.json("No blog items found");
  }
});

// Create a blog item
app.post("/blogs", requireAuth, async (req, res) => {
  const auth0Id = req.auth.payload.sub;
  const { title, desc, category } = req.body;

  if (!title || !desc || !category) {
    res.status(400).send("title, desc, and category are required");
  } else {
    const newBlogItem = await prisma.blogItem.create({
      data: {
        title,
        desc,
        category,

        User: { connect: { auth0Id } },
      },
    });

    res.status(201).json(newBlogItem);
  }
});

// Update a blog item by id
app.put("/blogs/:id", requireAuth, async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const { title, desc, category } = req.body;

    // Find the blog item by id along with its associated user
    const blogItem = await prisma.blogItem.findUnique({
      where: { id },
      include: { User: true }, // Include the associated user
    });

    // Check if the blog item exists
    if (!blogItem) {
      return res.status(404).json({ error: "Blog item not found" });
    }

    // Extract the client's Auth0 ID from the request payload
    const auth0Id = req.auth.payload.sub;

    // Check if the client's Auth0 ID matches the blog item's associated user's Auth0 ID
    if (blogItem.User.auth0Id !== auth0Id) {
      return res.status(403).json({ error: "Not authorized" });
    }

    // Update the blog item
    const updatedBlogItem = await prisma.blogItem.update({
      where: { id },
      data: { title, desc, category },
    });

    res.json(updatedBlogItem);
  } catch (error) {
    console.error("Error updating blog item:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Delete a blog item by id
app.delete("/blogs/:id", requireAuth, async (req, res) => {
  const id = Number(req.params.id);
  const userId = req.auth.payload.sub;

  const user = await prisma.User.findUnique({
    where: {
      auth0Id: userId,
    },
  });

  if (!user) {
    return res.status(404).json({ error: "User not found" });
  }

  const blogItem = await prisma.BlogItem.findFirst({
    where: {
      id,
      userId: user.id,
    },
  });

  if (!blogItem) {
    return res.json({ error: "Blog post not found" });
  }

  const deletedBlogItem = await prisma.BlogItem.delete({
    where: {
      id,
    },
  });

  res.status(200).json(deletedBlogItem);
});

// Get a blog item by id
app.get("/blogs/:id", async (req, res) => {
  const id = Number(req.params.id);
  const blogItem = await prisma.blogItem.findUnique({
    where: {
      id,
    },
    include: {
      User: true, // Include the related User record
      Comments: true, // Include the related Comment records
    },
  });
  res.status(200).json(blogItem);
});

// Create a comment
app.post("/blogs/:blogId/comments", async (req, res) => {
  try {
    // Extract data from request body
    const { text } = req.body;
    const { blogId } = req.params;

    const blog = await prisma.blogItem.findUnique({
      where: { id: parseInt(blogId) },
    });

    if (!blog) {
      return res.status(404).json({ error: "Blog not found" });
    }
    // Use PrismaClient to create a comment
    const comment = await prisma.comment.create({
      data: {
        text,
        blogItemId: parseInt(blogId),
      },
    });

    // Send the created comment as response
    res.json(comment);
  } catch (error) {
    // Handle errors
    console.error("Error creating comment:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

//veryfy user
app.post("/verify-user", requireAuth, async (req, res) => {
  const auth0Id = req.auth.payload.sub;
  const email = req.auth.payload[`${process.env.AUTH0_AUDIENCE}/email`];
  const name = req.auth.payload[`${process.env.AUTH0_AUDIENCE}/name`];

  const user = await prisma.user.findUnique({
    where: {
      auth0Id,
    },
  });
  // if the email is missing from the payload we will return an error
  if (!email) {
    return res.status(400).json({ error: "Email is missing from the payload" });
  }
  if (user) {
    res.json(user);
  } else {
    const newUser = await prisma.user.create({
      data: {
        email,
        auth0Id,
        name,
      },
    });

    res.json(newUser);
  }
});

//get current user infomation
app.get("/profile", requireAuth, async (req, res) => {
  const auth0Id = req.auth.payload.sub;
  try {
    const user = await prisma.user.findUnique({
      where: {
        auth0Id,
      },
    });
    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }
    res.json(user);
  } catch (err) {
    res.status(500).json({ error: "Internal server error" });
  }
});

//update user infomation
app.patch("/users/:id", requireAuth, async (req, res) => {
  const { bio } = req.body;
  const auth0Id = req.auth.payload.sub;

  try {
    const user = await prisma.user.findUnique({
      where: { auth0Id },
    });

    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }

    const updatedUser = await prisma.user.update({
      where: { auth0Id },
      data: { bio },
    });

    res.json(updatedUser);
  } catch (error) {
    console.error("Error updating user bio:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

const PORT = parseInt (process.env.PORT)||8000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT} 🎉 🚀`);
});
