import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Link } from "react-router-dom";
import Header from "@/components/Header";
import partnersImage from "@/assets/insurance-partners.png";

const Commercial = () => {
  const commercialInsuranceTypes = [
    {
      title: "Business Owners Policy (BOP)",
      description: "A comprehensive package that combines general liability and commercial property insurance at a cost-effective price. Perfect for small to medium-sized businesses looking for essential coverage.",
      icon: "🏢"
    },
    {
      title: "General Liability Insurance",
      description: "Protects your business from claims of bodily injury, property damage, and personal injury. Essential coverage for any business that interacts with customers or the public.",
      icon: "🛡️"
    },
    {
      title: "Commercial Auto Insurance",
      description: "Coverage for vehicles used in your business operations. Protects company cars, trucks, vans, and other commercial vehicles against accidents, theft, and damage.",
      icon: "🚛"
    },
    {
      title: "Workers' Compensation",
      description: "Required by law in most states, this coverage protects your employees and your business from workplace injuries and illnesses. Covers medical expenses and lost wages.",
      icon: "👷"
    },
    {
      title: "Commercial Property Insurance",
      description: "Protects your business property including buildings, equipment, inventory, and furniture from fire, theft, vandalism, and other covered perils.",
      icon: "🏭"
    },
    {
      title: "Professional Liability Insurance",
      description: "Also known as Errors & Omissions (E&O) insurance, this protects professionals from claims of negligence, mistakes, or failure to deliver promised services.",
      icon: "⚖️"
    },
    {
      title: "Commercial Umbrella Insurance",
      description: "Provides additional liability coverage beyond your primary commercial policies. Extra protection when claims exceed your standard policy limits.",
      icon: "☂️"
    },
    {
      title: "Cyber Liability Insurance",
      description: "Protects your business from cyber attacks, data breaches, and other technology-related risks. Covers data recovery, legal fees, and customer notification costs.",
      icon: "🔒"
    },
    {
      title: "Trucking Insurance",
      description: "Specialized coverage for trucking companies and owner-operators. Includes motor truck cargo, non-trucking liability, and other transportation-specific coverages.",
      icon: "🚚"
    },
    {
      title: "Directors & Officers (D&O)",
      description: "Protects company directors and officers from personal liability for decisions and actions taken in their professional capacity. Essential for corporations and nonprofits.",
      icon: "👔"
    },
    {
      title: "Employment Practices Liability",
      description: "Covers claims from employees alleging discrimination, harassment, wrongful termination, or other employment-related issues.",
      icon: "📋"
    },
    {
      title: "Garage Liability Insurance",
      description: "Specialized coverage for auto dealerships, repair shops, and parking facilities. Protects against risks unique to automotive businesses.",
      icon: "🔧"
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-brand-blue/20 to-brand-orange/20 py-16 lg:py-24">
        <div className="absolute inset-0 bg-[url('/api/placeholder/1920/600')] bg-cover bg-center opacity-20"></div>
        <div className="relative container mx-auto px-4 text-center">
          <h1 className="text-3xl lg:text-4xl font-bold text-foreground mb-4 max-w-4xl mx-auto">
            Comprehensive Commercial Insurance Solutions for Your Business
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Protect your business with tailored insurance coverage that grows with your company. 
            From startups to established enterprises, we have the expertise to keep you covered.
          </p>
        </div>
      </section>

      {/* Policies Section Header */}
      <section className="py-12 bg-background">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-2xl lg:text-3xl font-bold text-brand-blue mb-4">
            Commercial Insurance Policies We Offer
          </h2>
          <p className="text-lg text-muted-foreground mb-8 max-w-3xl mx-auto">
            Business Owners Policy, General Liability, Trucking, Commercial Umbrella, Commercial Autos, Workers Comp & so much More.
          </p>
          
          {/* Insurance Partners Logo */}
          <div className="flex justify-center mb-12">
            <img 
              src={partnersImage} 
              alt="Insurance Partner Companies" 
              className="max-w-md h-auto"
            />
          </div>
        </div>
      </section>

      {/* Insurance Types Grid */}
      <section className="py-16 bg-background">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {commercialInsuranceTypes.map((insurance, index) => (
              <Card key={index} className="overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                <CardContent className="p-6">
                  <div className="text-4xl mb-4 text-center">
                    {insurance.icon}
                  </div>
                  <h3 className="text-xl font-bold text-brand-blue mb-4 text-center">
                    {insurance.title}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed mb-6 text-center">
                    {insurance.description}
                  </p>
                  <Link to="/get-a-quote">
                    <Button 
                      className="w-full bg-brand-blue hover:bg-brand-blue/90 text-white font-semibold"
                      size="lg"
                    >
                      Get a Quote
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Industry Specialization Section */}
      <section className="py-16 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-2xl lg:text-3xl font-bold text-foreground mb-4">
              Industries We Serve
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Our experienced team understands the unique risks and challenges facing different industries.
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {[
              "Construction", "Transportation", "Healthcare", "Technology",
              "Manufacturing", "Retail", "Restaurants", "Professional Services",
              "Real Estate", "Education", "Non-Profit", "Agriculture"
            ].map((industry, index) => (
              <div key={index} className="bg-white rounded-lg p-4 text-center shadow-sm hover:shadow-md transition-shadow">
                <span className="font-semibold text-foreground">{industry}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Why Choose Us Section */}
      <section className="py-16 bg-background">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-2xl lg:text-3xl font-bold text-foreground mb-4">
              Why Choose Our Commercial Insurance?
            </h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-brand-orange to-brand-blue rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-white font-bold text-xl">🎯</span>
              </div>
              <h3 className="text-xl font-bold text-foreground mb-3">Tailored Solutions</h3>
              <p className="text-muted-foreground">Custom insurance packages designed specifically for your business needs and industry risks.</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-brand-orange to-brand-blue rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-white font-bold text-xl">🤝</span>
              </div>
              <h3 className="text-xl font-bold text-foreground mb-3">Expert Guidance</h3>
              <p className="text-muted-foreground">Our experienced agents work with you to understand your risks and find the right coverage.</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-brand-orange to-brand-blue rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-white font-bold text-xl">💰</span>
              </div>
              <h3 className="text-xl font-bold text-foreground mb-3">Competitive Rates</h3>
              <p className="text-muted-foreground">As an independent agency, we shop multiple carriers to find you the best coverage at competitive prices.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action Section */}
      <section className="py-16 bg-gradient-to-r from-brand-blue/10 to-brand-orange/10">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-2xl lg:text-3xl font-bold text-foreground mb-4">
            Ready to Protect Your Business?
          </h2>
          <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
            Don't leave your business exposed to risk. Our commercial insurance experts are ready to help you find the perfect coverage for your company.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/get-a-quote">
              <Button 
                size="lg" 
                className="bg-brand-blue hover:bg-brand-blue/90 text-white px-8"
              >
                Get Your Business Quote
              </Button>
            </Link>
            <Button 
              size="lg" 
              variant="outline" 
              className="border-brand-orange text-brand-orange hover:bg-brand-orange hover:text-white px-8"
            >
              Call (916) 772-4006
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Commercial;