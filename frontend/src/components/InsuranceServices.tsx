import InsuranceCard from "./InsuranceCard";
import personalImage from "@/assets/personal-insurance.jpg";
import commercialImage from "@/assets/commercial-insurance.jpg";
import partnersImage from "@/assets/insurance-partners.png";

const InsuranceServices = () => {
  const services = [
    {
      title: "Personal Lines Insurance",
      description: "Auto, Home, Umbrella, Renters, Landlord, Vacant, Motorcycle, RV, Boat, CEA, FLOOD, CA Fair Plan and more..",
      quote: "Some things in life are just wrong. Don't let your insurance be one of them. Let us do the right thing for you!",
      image: personalImage,
      alt: "Beautiful modern house representing personal insurance coverage"
    },
    {
      title: "Commercial Insurance", 
      description: "Business Owners Policy, General Liability, Trucking, Commercial Umbrella, Commercial Autos, Workers Comp & so much More.",
      quote: "They say risk is the secret to success. Let us help protect your risk today!",
      image: commercialImage,
      alt: "Modern business building representing commercial insurance"
    },
    {
      title: "Life & Health Insurance",
      description: "Life Insurance, Mortgage Protection, Retirement, Health Insurance.",
      quote: "Fun is like life insurance, the older you get the more it costs you. Take this as your sign today and get covered.",
      image: partnersImage,
      alt: "Insurance company partners and logos"
    }
  ];

  return (
    <section className="py-16 lg:py-24 bg-background">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 lg:gap-12">
          {services.map((service, index) => (
            <InsuranceCard
              key={index}
              title={service.title}
              description={service.description}
              quote={service.quote}
              image={service.image}
              alt={service.alt}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default InsuranceServices;