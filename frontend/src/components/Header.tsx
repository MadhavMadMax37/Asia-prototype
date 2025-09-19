import { useState } from "react";
import { Button } from "@/components/ui/button";
import { HoverCard, HoverCardTrigger, HoverCardContent } from "@/components/ui/hover-card";
import QuoteModal from "@/components/QuoteModal";
const logo = "/lovable-uploads/7b6edfe8-8717-443b-9999-168694fc2142.png";

const Header = () => {
  const [isQuoteModalOpen, setIsQuoteModalOpen] = useState(false);
  
  const navItems = [
    "HOME",
    "ABOUT US", 
    "PERSONAL",
    "COMMERCIAL",
    "CLIENT CENTER",
    "GET A QUOTE",
    "CAREERS",
    "FOR AGENTS ONLY"
  ];

  return (
    <header className="bg-background shadow-sm border-b">
      <div className="container mx-auto px-4 py-4">
        {/* Top section with logo and contact */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-4">
            <img 
              src={logo} 
              alt="ASIA Insurance Agency Logo" 
              className="h-16 w-auto"
            />
            <div className="text-left">
              <h1 className="text-2xl font-bold text-foreground tracking-tight">
                AMANDEEP SINGH
              </h1>
              <h2 className="text-lg font-semibold text-brand-blue">
                INSURANCE AGENCY
              </h2>
              <p className="text-sm text-brand-orange font-medium italic">
                "The Team you can Trust"
              </p>
            </div>
          </div>
          <Button 
            variant="default" 
            className="bg-brand-blue hover:bg-brand-blue/90 text-white px-6 py-2 rounded-full font-semibold"
            onClick={() => setIsQuoteModalOpen(true)}
          >
            GET A QUOTE
          </Button>
        </div>
        
        {/* Navigation */}
        <nav className="flex justify-center">
          <ul className="flex flex-wrap items-center justify-center space-x-6 lg:space-x-8">
            {navItems.map((item, index) => (
              <li key={index}>
                {item === "GET A QUOTE" ? (
                  <button
                    onClick={() => setIsQuoteModalOpen(true)}
                    className="text-sm font-semibold text-foreground hover:text-brand-orange transition-colors duration-200 tracking-wide"
                  >
                    {item}
                  </button>
                ) : item === "FOR AGENTS ONLY" ? (
                  <HoverCard>
                    <HoverCardTrigger asChild>
                      <button className="text-sm font-semibold text-foreground hover:text-brand-orange transition-colors duration-200 tracking-wide">
                        {item}
                      </button>
                    </HoverCardTrigger>
                    <HoverCardContent className="w-48 bg-background border shadow-lg">
                      <div className="space-y-2">
                        <a href="/partner-acelerate" className="block px-3 py-2 text-sm font-medium text-foreground hover:bg-muted hover:text-brand-orange rounded">
                          PARTNER ACELERATE
                        </a>
                        <a href="/acelerate-referral" className="block px-3 py-2 text-sm font-medium text-foreground hover:bg-muted hover:text-brand-orange rounded">
                          PARTNER REFERRAL
                        </a>
                        <a href="#" className="block px-3 py-2 text-sm font-medium text-foreground hover:bg-muted hover:text-brand-orange rounded">
                          NBT FORM
                        </a>
                        <a href="/dime-calculator" className="block px-3 py-2 text-sm font-medium text-foreground hover:bg-muted hover:text-brand-orange rounded">
                          DIME CALCULATOR
                        </a>
                        <a href="#" className="block px-3 py-2 text-sm font-medium text-foreground hover:bg-muted hover:text-brand-orange rounded">
                          NEW PAGE
                        </a>
                      </div>
                    </HoverCardContent>
                  </HoverCard>
                ) : (
                  <a 
                    href={
                      item === "ABOUT US" ? "/about-us" :
                      item === "PERSONAL" ? "/personal" :
                      item === "COMMERCIAL" ? "/commercial" :
                      item === "CLIENT CENTER" ? "/client-center" :
                      item === "CAREERS" ? "/careers" :
                      item === "HOME" ? "/" : "#"
                    } 
                    className="text-sm font-semibold text-foreground hover:text-brand-orange transition-colors duration-200 tracking-wide"
                  >
                    {item}
                  </a>
                )}
              </li>
            ))}
          </ul>
        </nav>
      </div>
      
      <QuoteModal 
        open={isQuoteModalOpen} 
        onOpenChange={setIsQuoteModalOpen} 
      />
    </header>
  );
};

export default Header;