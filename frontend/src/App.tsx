import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import AboutUs from "./pages/AboutUs";
import Personal from "./pages/Personal";
import Commercial from "./pages/Commercial";
import ClientCenter from "./pages/ClientCenter";
import GetAQuote from "./pages/GetAQuote";
import Careers from "./pages/Careers";
import PartnerAcelerate from "./pages/PartnerAcelerate";
import AcelerateReferral from "./pages/AcelerateReferral";
import DimeCalculator from "./pages/DimeCalculator";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/about-us" element={<AboutUs />} />
          <Route path="/personal" element={<Personal />} />
          <Route path="/commercial" element={<Commercial />} />
          <Route path="/client-center" element={<ClientCenter />} />
          <Route path="/get-a-quote" element={<GetAQuote />} />
          <Route path="/careers" element={<Careers />} />
          <Route path="/partner-acelerate" element={<PartnerAcelerate />} />
          <Route path="/acelerate-referral" element={<AcelerateReferral />} />
          <Route path="/dime-calculator" element={<DimeCalculator />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
