const HeroSection = () => {
  return (
    <section className="bg-hero-gradient py-16 lg:py-24">
      <div className="container mx-auto px-4 text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl lg:text-6xl font-bold text-foreground mb-8 leading-tight">
            <span className="block">Coverage you deserve,</span>
            <span className="block">Rates you can afford,</span>
            <span className="block">
              All from an Agency you can{" "}
              <span className="text-brand-orange">TRUST!</span>
            </span>
          </h1>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;