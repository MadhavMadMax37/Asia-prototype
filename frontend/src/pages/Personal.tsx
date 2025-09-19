import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Link } from "react-router-dom";
import Header from "@/components/Header";
import partnersImage from "@/assets/insurance-partners.png";

const Personal = () => {
  const insuranceTypes = [
    {
      title: "Life Insurance",
      description: "Life is unpredictable, and none of us can foresee what the future holds. However, you can take steps today to secure the financial well-being of your loved ones in the event of your passing. Life insurance is a powerful financial tool that provides peace of mind, ensuring that your family is protected and financially stable when you're no longer there. Our comprehensive life insurance plans are designed to safeguard your loved ones' future, offering you the assurance that they will be taken care of, even in your absence.",
      image: "/api/placeholder/500/300"
    },
    {
      title: "Auto Insurance", 
      description: "CA State Minimum Liability Coverage: $30k Bodily Injury, $60k Bodily Injury Limit Per Accident, $15k Property Damage. For most these limits are just not enough to cover an accident in CA. Let us help you find coverage you need at prices you can afford!",
      image: "/api/placeholder/500/300"
    },
    {
      title: "HOME INSURANCE",
      description: "Are you looking to purchase a home? Need help in finding the coverage you need? We are here to help navigate and provide coverage to your home. Whether space you call home from mobile homes, condos, duplexes, to single family homes and more we will help find the coverage you need. Most home insurance policy's do not cover perils of Earthquake and Flood. These policies require separate policies to be purchased.",
      image: "/api/placeholder/500/300"
    },
    {
      title: "Renters Insurance", 
      description: "Just because you rent doesn't mean you shouldn't protect your belongings. Renters insurance protects your personal property and provides liability coverage in case someone is injured in your rental home.",
      image: "/api/placeholder/500/300"
    },
    {
      title: "Landlord Insurance",
      description: "Protect your rental property investment with comprehensive landlord insurance. Coverage includes property protection, loss of rental income, and liability protection for property owners.",
      image: "/api/placeholder/500/300"
    },
    {
      title: "Motorcycle Insurance",
      description: "Hit the road with confidence knowing you're protected. Our motorcycle insurance provides coverage for your bike, gear, and liability protection while you enjoy the ride.",
      image: "/api/placeholder/500/300"
    },
    {
      title: "RV Insurance",
      description: "Whether you're a weekend warrior or a full-time RVer, protect your home away from home with comprehensive RV insurance coverage tailored to your lifestyle.",
      image: "/api/placeholder/500/300"
    },
    {
      title: "Boat Insurance",
      description: "From fishing boats to luxury yachts, protect your vessel and enjoy peace of mind on the water with our comprehensive marine insurance coverage.",
      image: "/api/placeholder/500/300"
    },
    {
      title: "Umbrella Insurance",
      description: "Extra liability protection that goes beyond your standard auto and home insurance limits. Umbrella insurance provides additional coverage when you need it most.",
      image: "/api/placeholder/500/300"
    },
    {
      title: "Flood Insurance",
      description: "Standard homeowners insurance doesn't cover flood damage. Protect your home and belongings with dedicated flood insurance coverage through the National Flood Insurance Program.",
      image: "/api/placeholder/500/300"
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-muted/50 to-muted/30 py-16 lg:py-24">
        <div className="absolute inset-0 bg-[url('/api/placeholder/1920/600')] bg-cover bg-center opacity-20"></div>
        <div className="relative container mx-auto px-4 text-center">
          <h1 className="text-3xl lg:text-4xl font-bold text-foreground mb-4 max-w-4xl mx-auto">
            Protect Your Personal Property With An Agency That Has Your Needs Ahead Of Their Own.
          </h1>
        </div>
      </section>

      {/* Policies Section Header */}
      <section className="py-12 bg-background">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-2xl lg:text-3xl font-bold text-brand-blue mb-8">
            Personal Insurance Policies We Offer
          </h2>
          
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
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {insuranceTypes.map((insurance, index) => (
              <Card key={index} className="overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300">
                <div className="aspect-video bg-muted flex items-center justify-center">
                  <div className="w-16 h-16 bg-gradient-to-br from-brand-orange to-brand-blue rounded-full flex items-center justify-center">
                    <span className="text-white font-bold text-lg">
                      {insurance.title.split(' ')[0][0]}
                    </span>
                  </div>
                </div>
                <CardContent className="p-6">
                  <h3 className="text-xl lg:text-2xl font-bold text-brand-blue mb-4">
                    {insurance.title}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed mb-6">
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

      {/* Call to Action Section */}
      <section className="py-16 bg-gradient-to-r from-brand-blue/10 to-brand-orange/10">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-2xl lg:text-3xl font-bold text-foreground mb-4">
            Ready to Protect What Matters Most?
          </h2>
          <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
            Our experienced team is here to help you find the right coverage for your personal insurance needs. 
            Contact us today for a personalized quote.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/get-a-quote">
              <Button 
                size="lg" 
                className="bg-brand-blue hover:bg-brand-blue/90 text-white px-8"
              >
                Get Your Quote Now
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

export default Personal;