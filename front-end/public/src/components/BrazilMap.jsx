import React from 'react';
import { ComposableMap, Geographies, Geography } from 'react-simple-maps';

const BRAZIL_GEO_URL = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson";

const BrazilMap = ({ onStateClick }) => {
  return (
    <ComposableMap
      projection="geoMercator"
      projectionConfig={{
        scale: 700,
        center: [-54, -15]
      }}
      style={{ width: "100%", height: "auto" }}
    >
      <Geographies geography={BRAZIL_GEO_URL}>
        {({ geographies }) =>
          geographies.map(geo => (
            <Geography
              key={geo.rsmKey}
              geography={geo}
              onClick={() => {
                const { name, sigla } = geo.properties;
                onStateClick({ nome: name, sigla: sigla });
              }}
              style={{
                default: { fill: "#D6D6DA", outline: "none" },
                hover: { fill: "#F53", outline: "none" },
                pressed: { fill: "#E42", outline: "none" },
              }}
            />
          ))
        }
      </Geographies>
    </ComposableMap>
  );
};

export default BrazilMap;