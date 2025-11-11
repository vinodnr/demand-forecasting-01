module.exports = {
  webServer: {
    command: 'npm run dev',
    port: 3000,
    cwd: process.cwd()
  },
  use: { headless: true }
}
