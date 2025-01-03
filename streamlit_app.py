import React, { useState, useEffect, useCallback } from 'react';

const FlappyBird = () => {
  const [gameStarted, setGameStarted] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [score, setScore] = useState(0);
  const [birdPosition, setBirdPosition] = useState(250);
  const [birdVelocity, setBirdVelocity] = useState(0);
  const [pipes, setPipes] = useState([]);
  
  const GRAVITY = 0.5;
  const JUMP_FORCE = -8;
  const PIPE_SPEED = 3;
  const PIPE_SPAWN_RATE = 1500;
  const PIPE_GAP = 150;
  const PIPE_WIDTH = 52;
  
  useEffect(() => {
    if (!gameStarted || gameOver) return;
    
    const gameLoop = setInterval(() => {
      setBirdPosition(pos => {
        const newPos = pos + birdVelocity;
        if (newPos > 500 || newPos < 0) {
          setGameOver(true);
          return pos;
        }
        return newPos;
      });
      
      setBirdVelocity(vel => vel + GRAVITY);
      
      setPipes(currentPipes => {
        return currentPipes
          .map(pipe => ({
            ...pipe,
            x: pipe.x - PIPE_SPEED
          }))
          .filter(pipe => pipe.x > -60);
      });
      
      pipes.forEach(pipe => {
        const birdBox = {
          left: 50,
          right: 86,
          top: birdPosition,
          bottom: birdPosition + 36
        };
        
        const topPipeBox = {
          left: pipe.x,
          right: pipe.x + PIPE_WIDTH,
          top: 0,
          bottom: pipe.height
        };
        
        const bottomPipeBox = {
          left: pipe.x,
          right: pipe.x + PIPE_WIDTH,
          top: pipe.height + PIPE_GAP,
          bottom: 500
        };
        
        if (
          (birdBox.right > topPipeBox.left && 
           birdBox.left < topPipeBox.right && 
           birdBox.top < topPipeBox.bottom) ||
          (birdBox.right > bottomPipeBox.left && 
           birdBox.left < bottomPipeBox.right && 
           birdBox.bottom > bottomPipeBox.top)
        ) {
          setGameOver(true);
        }
        
        if (pipe.x === 48) {
          setScore(s => s + 1);
        }
      });
    }, 16);
    
    return () => clearInterval(gameLoop);
  }, [gameStarted, gameOver, birdPosition, birdVelocity, pipes]);
  
  useEffect(() => {
    if (!gameStarted || gameOver) return;
    
    const spawnPipe = setInterval(() => {
      const height = Math.floor(Math.random() * (300 - 100) + 100);
      setPipes(currentPipes => [...currentPipes, { x: 400, height }]);
    }, PIPE_SPAWN_RATE);
    
    return () => clearInterval(spawnPipe);
  }, [gameStarted, gameOver]);
  
  const handleJump = useCallback(() => {
    if (!gameStarted) {
      setGameStarted(true);
    }
    if (!gameOver) {
      setBirdVelocity(JUMP_FORCE);
    }
  }, [gameStarted, gameOver]);
  
  const handleRestart = () => {
    setGameStarted(false);
    setGameOver(false);
    setScore(0);
    setBirdPosition(250);
    setBirdVelocity(0);
    setPipes([]);
  };

  const PipeSection = ({ isTop, height, x }) => (
    <div
      className="absolute"
      style={{
        left: x,
        width: PIPE_WIDTH,
        height: isTop ? height : `calc(100% - ${height + PIPE_GAP}px)`,
        top: isTop ? 0 : height + PIPE_GAP,
      }}
    >
      {/* Main pipe body */}
      <div className="absolute inset-0 bg-green-600 border-l-4 border-r-4 border-green-900" />
      
      {/* Pipe cap */}
      <div 
        className="absolute left-[-8px] right-[-8px] h-10 bg-green-600 border-4 border-green-900"
        style={{
          top: isTop ? 'auto' : 0,
          bottom: isTop ? 0 : 'auto',
        }}
      />
    </div>
  );
  
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-blue-100">
      <div className="relative w-96 h-[500px] bg-blue-300 overflow-hidden">
        {/* Bird */}
        <div 
          className="absolute w-9 h-9 bg-yellow-400 rounded-full"
          style={{ 
            top: birdPosition,
            left: 50,
            transform: `rotate(${birdVelocity * 4}deg)`,
            transition: 'transform 0.1s'
          }}
        />
        
        {/* Pipes */}
        {pipes.map((pipe, index) => (
          <React.Fragment key={index}>
            <PipeSection isTop={true} height={pipe.height} x={pipe.x} />
            <PipeSection isTop={false} height={pipe.height} x={pipe.x} />
          </React.Fragment>
        ))}
        
        {/* Score */}
        <div className="absolute top-4 left-4 text-4xl font-bold text-white">
          {score}
        </div>
        
        {/* Start/Game Over message */}
        {!gameStarted && (
          <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="text-white text-2xl font-bold text-center">
              Click or Press Space<br/>to Start
            </div>
          </div>
        )}
        {gameOver && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-black bg-opacity-50">
            <div className="text-white text-2xl font-bold mb-4">
              Game Over!<br/>
              Score: {score}
            </div>
            <button
              className="px-4 py-2 bg-white text-black rounded hover:bg-gray-200"
              onClick={handleRestart}
            >
              Play Again
            </button>
          </div>
        )}
      </div>
      
      {/* Controls */}
      <button
        className="mt-4 px-8 py-4 bg-blue-500 text-white rounded-full text-xl font-bold hover:bg-blue-600 active:bg-blue-700"
        onClick={handleJump}
      >
        JUMP
      </button>
    </div>
  );
};

export default FlappyBird;
