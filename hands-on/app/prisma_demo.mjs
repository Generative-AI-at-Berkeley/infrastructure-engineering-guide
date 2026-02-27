import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  const created = await prisma.student.create({
    data: {
      name: "Grace Hopper",
      classYear: 4,
      email: "grace@example.com",
    },
  });

  const rows = await prisma.student.findMany({
    orderBy: { id: "desc" },
    take: 5,
  });

  console.log("Inserted via Prisma:");
  console.log(created);
  console.log("Recent students:");
  console.log(rows);
}

main()
  .catch((err) => {
    console.error(err);
    process.exitCode = 1;
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
