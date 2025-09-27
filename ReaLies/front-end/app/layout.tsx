export const metadata = {
  title: 'ReaLies',
  description: 'Deep Learning Video Analysis Tool',
  icons: {
    icon: '/logo.png', // Langsung ke file .png
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}