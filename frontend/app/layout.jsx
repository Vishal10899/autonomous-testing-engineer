import './globals.css';
import Navbar from '../components/Navbar';

export const metadata = {
  title: 'Autonomous Testing Engineer — Command Center',
  description: 'World-Class Autonomous AI Software Testing & Production-Readiness Platform',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#090d16] text-gray-100 antialiased flex flex-col">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {children}
        </main>
      </body>
    </html>
  );
}
