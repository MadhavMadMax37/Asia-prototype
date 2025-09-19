import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Link } from "react-router-dom";

interface InsuranceCardProps {
  title: string;
  description: string;
  quote: string;
  image: string;
  alt: string;
}

const InsuranceCard = ({ title, description, quote, image, alt }: InsuranceCardProps) => {
  return (
    <Card className="overflow-hidden shadow-card hover:shadow-card-hover transition-all duration-300 hover:-translate-y-2 bg-card">
      <div className="aspect-video overflow-hidden">
        <img 
          src={image} 
          alt={alt}
          className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
        />
      </div>
      <div className="p-8">
        <h2 className="text-2xl font-bold text-brand-orange mb-4">
          {title}
        </h2>
        <p className="text-foreground font-semibold mb-4 leading-relaxed">
          {description}
        </p>
        <p className="text-muted-foreground italic mb-6 leading-relaxed">
          {quote}
        </p>
        <Link to="/get-a-quote">
          <Button 
            variant="default" 
            className="bg-brand-orange hover:bg-brand-orange/90 text-white font-semibold px-8 py-2 rounded-md transition-all duration-200"
          >
            Get A Quote
          </Button>
        </Link>
      </div>
    </Card>
  );
};

export default InsuranceCard;