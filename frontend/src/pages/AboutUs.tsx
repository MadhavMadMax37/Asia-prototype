import { Button } from "@/components/ui/button";
import Header from "@/components/Header";

const AboutUs = () => {
  const teamMembers = [
    {
      name: "BALDEV SINGH",
      role: "",
      description: "Its been a great honor to be able to serve my community here in the Greater Sacramento Area. I specialize in All Lines of Insurance and look forward to serving you for all your insurance needs!",
      email: "baldev@asiainc.co",
      phone: "+19167724006"
    },
    {
      name: "SANDEEP KUMAR", 
      role: "Commercial Lines Specialist/Trucking Specialist",
      description: "",
      email: "sandeep@asiainc.co",
      phone: "+19167724006"
    },
    {
      name: "Jennifer Wilson",
      role: "Personal Lines Specialist", 
      description: "",
      email: "jen@asiainc.co",
      phone: "+9167724006"
    },
    {
      name: "Simarjeet Singh",
      role: "Customer Service Specialist",
      description: "",
      email: "team@asiainc.co",
      phone: "Team@asiainc.co"
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-brand-orange/20 to-brand-blue/20 py-24">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl lg:text-5xl font-bold text-foreground mb-4">
            About Us
          </h1>
        </div>
      </section>

      {/* Main Content Section */}
      <section className="py-16 lg:py-24">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mb-16">
            {/* Left Side - Promotional Image */}
            <div className="flex justify-center">
              <div className="bg-gradient-to-b from-blue-500 to-blue-700 p-8 rounded-lg text-white text-center max-w-md">
                <h2 className="text-xl font-bold mb-4">HAVE ALL YOUR POLICIES UNDER ONE ROOF!</h2>
                <div className="text-4xl font-bold mb-2">AMANDEEP SINGH</div>
                <div className="text-2xl font-semibold mb-6">AGENCY</div>
                <div className="bg-white/10 p-4 rounded mb-6">
                  <div className="text-lg font-semibold mb-2">Coverage you deserve. Rates you can afford. All from an agency you can TRUST!</div>
                </div>
                <div className="text-sm mb-4">
                  <p>Personal Line Insurance: Auto, Homeowners, Renters, Landlord, Condo, Umbrella, Life, Health, Mortgage Protection, CA Fair Plan, Flood, Earthquake, Motorcycles, RVs, Boats and more...</p>
                  <p className="mt-2">Commercial Insurance: Workers Compensation, General Liability, Business Owners Policy, Commercial Auto, Trucking, Garage Liability, Commercial Umbrella, Builders Risk, E&O, and more...</p>
                </div>
                <div className="border-t border-white/20 pt-4">
                  <p className="font-semibold">Call/Email or Visit Us Today, Let us help you find the coverage you need.</p>
                  <p className="text-xl font-bold">(916)772-4006</p>
                  <p>team@amandeepsinghagency.com</p>
                </div>
              </div>
            </div>

            {/* Right Side - About Text */}
            <div className="space-y-6">
              <div className="text-lg leading-relaxed">
                <p className="font-semibold mb-4">
                  At Amandeep Singh Insurance Agency we have the tools and knowledge to get you the coverage you need at a price that you can afford.
                </p>
                <p className="mb-4">
                  The beauty of being an Independent Agency we work for you not for the Insurance Carriers that means we can do the shopping for you and find the best coverages at great rates so we let you decide.
                </p>
                <p className="mb-4">
                  Have questions about your insurance? We take pride in sharing our knowledge with our clients so you don't get on the road and ever wonder if your covered.
                </p>
                <p className="font-semibold">
                  Here at Amandeep Singh Agency, we value our clients and look forward to serving you for all of your insurance needs!
                </p>
              </div>
            </div>
          </div>

          {/* Team Section */}
          <div className="mt-16">
            <h2 className="text-3xl font-bold text-center mb-12 text-foreground">Meet the Team</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {teamMembers.map((member, index) => (
                <div key={index} className="bg-card rounded-lg p-6 shadow-md border">
                  <div className="text-center">
                    <div className="w-24 h-24 bg-gradient-to-br from-brand-orange to-brand-blue rounded-full mx-auto mb-4 flex items-center justify-center">
                      <span className="text-2xl font-bold text-white">
                        {member.name.split(' ').map(n => n[0]).join('')}
                      </span>
                    </div>
                    <h3 className="text-xl font-bold text-foreground mb-2">{member.name}</h3>
                    {member.role && (
                      <p className="text-brand-orange font-semibold mb-3">{member.role}</p>
                    )}
                    {member.description && (
                      <p className="text-muted-foreground mb-4 text-sm leading-relaxed">{member.description}</p>
                    )}
                    <div className="space-y-2">
                      <p className="text-sm">
                        <a href={`mailto:${member.email}`} className="text-brand-blue hover:underline">
                          {member.email}
                        </a>
                      </p>
                      <Button 
                        variant="default" 
                        size="sm" 
                        className="w-full bg-brand-blue hover:bg-brand-blue/90"
                        onClick={() => {
                          if (member.phone.includes('@')) {
                            window.location.href = `mailto:${member.phone}`;
                          } else {
                            window.location.href = `tel:${member.phone}`;
                          }
                        }}
                      >
                        Contact Me
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AboutUs;