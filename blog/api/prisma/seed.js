import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  const alice = await prisma.user.upsert({
    where: { email: "alice@prisma.io" },
    update: {},
    create: {
      email: "alice@prisma.io",
      auth0Id: "aliceAuth0Id",
      name: "Alice",

      BlogItem: {
        create: {
          title: "Lorem ipsum dolor sit amet consectetur adipisicing elit",
          desc: "<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. A possimus excepturi aliquid nihil cumque ipsam facere aperiam at! Ea dolorem ratione sit debitis deserunt repellendus numquam ab vel perspiciatis corporis!</p>",
          img: "https://images.pexels.com/photos/7008010/pexels-photo-7008010.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
          category: "art",
        },
      },
    },
  });

  const bob = await prisma.user.upsert({
    where: { email: "bob@prisma.io" },
    update: {},
    create: {
      email: "bob@prisma.io",
      auth0Id: "google-oauth2|117931933326448414992",
      name: "Bob",
      BlogItem: {
        create: [
          {
            title: "Lorem ipsum dolor sit amet consectetur adipisicing elit",
            desc: "<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. A possimus excepturi aliquid nihil cumque ipsam facere aperiam at! Ea dolorem ratione sit debitis deserunt repellendus numquam ab vel perspiciatis corporis!</p>",
            img: "https://images.pexels.com/photos/6489663/pexels-photo-6489663.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
            category: "science",
          },
          {
            title: "Lorem ipsum dolor sit amet consectetur adipisicing elit",
            desc: "<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. A possimus excepturi aliquid nihil cumque ipsam facere aperiam at! Ea dolorem ratione sit debitis deserunt repellendus numquam ab vel perspiciatis corporis!</p>",
            img: "https://images.pexels.com/photos/2582937/pexels-photo-2582937.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
            category: "technology",
          },
          {
            title: "1 Lorem ipsum dolor sit amet consectetur adipisicing elit",
            desc: "<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. A possimus excepturi aliquid nihil cumque ipsam facere aperiam at! Ea dolorem ratione sit debitis deserunt repellendus numquam ab vel perspiciatis corporis!</p>",
            img: "https://images.pexels.com/photos/3945313/pexels-photo-3945313.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
            category: "cinema",
          },
          {
            title: "2 Lorem ipsum dolor sit amet consectetur adipisicing elit",
            desc: "<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. A possimus excepturi aliquid nihil cumque ipsam facere aperiam at! Ea dolorem ratione sit debitis deserunt repellendus numquam ab vel perspiciatis corporis!</p>",
            img: "https://images.pexels.com/photos/411214/pexels-photo-411214.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
            category: "cinema",
          },
        ],
      },
    },
  });
  const designUser = await prisma.user.upsert({
    where: { email: "design@prisma.io" },
    update: {},
    create: {
      email: "design@prisma.io",
      auth0Id: "designAuth0Id",
      name: "Design User",
      BlogItem: {
        create: {
          title: "Design Post Title",
          desc: "<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. A possimus excepturi aliquid nihil cumque ipsam facere aperiam at! Ea dolorem ratione sit debitis deserunt repellendus numquam ab vel perspiciatis corporis!</p>",
          img: "https://images.pexels.com/photos/1762851/pexels-photo-1762851.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
          category: "design",
        },
      },
    },
  });

  const foodUser = await prisma.user.upsert({
    where: { email: "food@prisma.io" },
    update: {},
    create: {
      email: "food@prisma.io",
      auth0Id: "foodAuth0Id",
      name: "Food User",
      BlogItem: {
        create: {
          title: "Food Post Title",
          desc: "<p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. A possimus excepturi aliquid nihil cumque ipsam facere aperiam at! Ea dolorem ratione sit debitis deserunt repellendus numquam ab vel perspiciatis corporis!</p>",
          img: "https://images.pexels.com/photos/6157049/pexels-photo-6157049.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
          category: "food",
        },
      },
    },
  });
  console.log({ alice, bob, designUser, foodUser });
}
main()
  .then(async () => {
    await prisma.$disconnect();
  })
  .catch(async (e) => {
    console.error(e);
    await prisma.$disconnect();
    process.exit(1);
  });
