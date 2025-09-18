import { Routes, Route } from 'react-router-dom'
import { Toaster } from '@/components/ui/toaster'
import Layout from '@/components/layout'
import HomePage from '@/pages/home'
import PoliticiansPage from '@/pages/politicians'
import PoliticianDetailsPage from '@/pages/politicians/details'
import BillsPage from '@/pages/bills'
import BillDetailsPage from '@/pages/bills/details'
import VotesPage from '@/pages/votes'
import ContributionsPage from '@/pages/contributions'
import NotFoundPage from '@/pages/not-found'
import { ThemeProvider } from '@/components/theme-provider'

function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="povodb-theme">
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="politicians" element={<PoliticiansPage />} />
          <Route path="politicians/:id" element={<PoliticianDetailsPage />} />
          <Route path="bills" element={<BillsPage />} />
          <Route path="bills/:id" element={<BillDetailsPage />} />
          <Route path="votes" element={<VotesPage />} />
          <Route path="contributions" element={<ContributionsPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
      <Toaster />
    </ThemeProvider>
  )
}

export default App
