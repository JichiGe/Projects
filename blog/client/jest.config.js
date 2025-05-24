module.exports = {
  testEnvironment: "node",

  testMatch: ["**/__tests__/**/*.[jt]s?(x)", "**/?(*.)+(spec|test).[tj]s?(x)"],

  moduleNameMapper: {
    "\\.(css|less)$": "identity-obj-proxy",
    "^@components/(.*)$": "<rootDir>/src/components/$1",
  },

  moduleDirectories: ["node_modules", "src"],

  transformIgnorePatterns: ["/node_modules/"],

  setupFilesAfterEnv: ["<rootDir>/setupTests.js"],
};
