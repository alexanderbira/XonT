import React from "react";

import { Socket } from 'socket.io-client';

import resultsStyles from "./results.module.css";

interface ResultsProps {
  socket: Socket;
}

export default function Results({ socket }: ResultsProps) {
  const [numCreated, setNumCreated] = React.useState(0);
  const [allLoaded, setAllLoaded] = React.useState(false);

  React.useEffect(() => {
    socket.emit("create_results");
    socket.on("next_completed", () => setNumCreated(n => n + 1));
    socket.on("all_completed", () => setAllLoaded(true));
  }, []);

  return (
    <div>
      {
        !allLoaded && <p>Generating model {numCreated + 1}...</p>
      }
      {/* Load all the completed models here */}
    </div>
  );
}
