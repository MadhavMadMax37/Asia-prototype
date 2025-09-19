import { useState } from "react";
import { Button } from "@/components/ui/button";
import Header from "@/components/Header";
import QuoteModal from "@/components/QuoteModal";

const GetAQuote = () => {
  const [isQuoteModalOpen, setIsQuoteModalOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      {/* Hero Section */}
      <section 
        className="relative bg-cover bg-center bg-no-repeat py-32 lg:py-48"
        style={{
          backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url('/api/placeholder/1920/800')`
        }}
      >
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-2xl mx-auto">
            <h1 className="text-4xl lg:text-5xl font-bold text-white mb-8">
              Get A Quote
            </h1>
            
            <div className="space-y-4">
              <Button 
                size="lg" 
                className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-full text-lg font-semibold"
                onClick={() => setIsQuoteModalOpen(true)}
              >
                Get a Quote
              </Button>
              
              <div className="block">
                <Button 
                  size="lg" 
                  className="bg-black hover:bg-gray-800 text-white px-8 py-4 rounded-full text-lg font-semibold"
                  onClick={() => setIsQuoteModalOpen(true)}
                >
                  Get A Quick Auto Quote
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer Section */}
      <section className="bg-brand-orange text-white py-16">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            
            {/* Company Info */}
            <div>
              <h3 className="text-2xl font-bold mb-4">A.S.I.A INC.</h3>
              <h4 className="text-xl font-semibold mb-4">Address</h4>
              <p className="text-lg leading-relaxed">
                3017 Douglas Blvd STE 140<br />
                Roseville, CA 95661
              </p>
            </div>

            {/* Hours */}
            <div>
              <h4 className="text-xl font-semibold mb-4">Hours</h4>
              <div className="space-y-2">
                <p className="text-lg">
                  <strong>Monday — Friday</strong><br />
                  9am — 5pm
                </p>
                <p className="text-lg">
                  <strong>Saturday — Sunday</strong><br />
                  by apt only
                </p>
              </div>
            </div>

            {/* Contact */}
            <div>
              <h4 className="text-xl font-semibold mb-4">Contact</h4>
              <div className="space-y-3 text-lg">
                <p>A.S.I.A Inc CA Lic#6009368</p>
                <p>
                  <a href="mailto:TEAM@ASIAINC.CO" className="hover:underline">
                    TEAM@ASIAINC.CO
                  </a>
                </p>
                <p>
                  <strong>Direct:</strong> 
                  <a href="tel:916-772-4006" className="hover:underline ml-1">
                    916-772-4006
                  </a>
                </p>
                <p>
                  <strong>Fax:</strong> 916-772-4007
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <QuoteModal 
        open={isQuoteModalOpen} 
        onOpenChange={setIsQuoteModalOpen} 
      />
    </div>
  );
};

export default GetAQuote;