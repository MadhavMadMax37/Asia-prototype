import Header from "@/components/Header";
import HeroSection from "@/components/HeroSection";
import InsuranceServices from "@/components/InsuranceServices";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main>
        <HeroSection />
        <InsuranceServices />
      </main>
    </div>
  );
};

export default Index;
