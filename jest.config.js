module.exports = {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.(ts|tsx)$': 'babel-jest',
  },
  moduleFileExtensions: ['ts','tsx','js','jsx','json','node'],
  setupFilesAfterEnv: ['<rootDir>/frontend/tests/setupTests.ts']
}
