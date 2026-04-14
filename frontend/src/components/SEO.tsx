import { Helmet } from 'react-helmet-async';

interface SEOProps {
  title: string;
  description: string;
  canonical?: string;
  ogImage?: string;
  noIndex?: boolean;
  jsonLd?: Record<string, any>;
}

const SEO = ({ 
  title, 
  description, 
  canonical, 
  ogImage = '/og-default.jpg', 
  noIndex = false 
}: SEOProps) => {
  const siteUrl = import.meta.env.VITE_SITE_URL || 'http://localhost:5173';
  const fullTitle = `${title} | Medication Reminder`;
  
  return (
    <Helmet>
      {/* Базовые теги */}
      <title>{fullTitle}</title>
      <meta name="description" content={description} />
      {noIndex && <meta name="robots" content="noindex, nofollow" />}
      
      {/* Canonical URL */}
      {canonical && <link rel="canonical" href={`${siteUrl}${canonical}`} />}

      
      {/* Open Graph / Social */}
      <meta property="og:title" content={fullTitle} />
      <meta property="og:description" content={description} />
      <meta property="og:type" content="website" />
      <meta property="og:url" content={`${siteUrl}${canonical || '/'}`} />
      <meta property="og:image" content={`${siteUrl}${ogImage}`} />
      <meta name="twitter:card" content="summary_large_image" />
      
      {/* Дополнительные */}
      <meta name="theme-color" content="#3b82f6" />
    </Helmet>
  );
};

export default SEO;