import React, { useState, useEffect } from 'react';

const FlappyBirdGame = () => {
  const [gameState, setGameState] = useState({
    birdY: 200,
    birdVelocity: 0,
    pipes: [],
    score: 0,
    isGameOver: false,
    isPlaying: false
  });

  const CANVAS_HEIGHT = 400;
  const CANVAS_WIDTH = 300;
  const BIRD_SIZE = 20;
  const PIPE_WIDTH = 40;
  const PIPE_GAP = 150;

  const resetGame = () => {
    setGameState({
      birdY: CANVAS_HEIGHT / 2,
      birdVelocity: 0,
      pipes: [],
      score: 0,
      isGameOver: false,
      isPlaying: true
    });
    spawnPipe();
  };

  const spawnPipe = () => {
    const newPipes = [...gameState.pipes];
    const pipeHeight = Math.random() * (CANVAS_HEIGHT - PIPE_GAP - 100) + 50;
    
    newPipes.push({
      x: CANVAS_WIDTH,
      topHeight: pipeHeight,
      bottomHeight: CANVAS_HEIGHT - pipeHeight - PIPE_GAP
    });

    setGameState(prev => ({
      ...prev,
      pipes: newPipes
    }));
  };

  const updateGame = () => {
    if (!gameState.isPlaying || gameState.isGameOver) return;

    // Apply gravity
    const newVelocity = gameState.birdVelocity + 0.5;
    const newBirdY = gameState.birdY + newVelocity;

    // Check ground/ceiling collision
    if (newBirdY >= CANVAS_HEIGHT - BIRD_SIZE || newBirdY <= 0) {
      setGameState(prev => ({
        ...prev,
        isGameOver: true,
        isPlaying: false
      }));
      return;
    }

    // Move and filter pipes
    const updatedPipes = gameState.pipes
      .map(pipe => ({ ...pipe, x: pipe.x - 3 }))
      .filter(pipe => pipe.x > -PIPE_WIDTH);

    // Spawn new pipes
    if (updatedPipes.length === 0 || 
        updatedPipes[updatedPipes.length - 1].x < CANVAS_WIDTH - 200) {
      spawnPipe();
    }

    // Collision detection
    const checkCollision = updatedPipes.some(pipe => 
      pipe.x < BIRD_SIZE && 
      pipe.x + PIPE_WIDTH > 0 && 
      (newBirdY < pipe.topHeight || 
       newBirdY > CANVAS_HEIGHT - pipe.bottomHeight)
    );

    if (checkCollision) {
      setGameState(prev => ({
        ...prev,
        isGameOver: true,
        isPlaying: false
      }));
      return;
    }

    // Update game state
    setGameState(prev => ({
      ...prev,
      birdY: newBirdY,
      birdVelocity: newVelocity,
      pipes: updatedPipes,
      score: prev.score + (updatedPipes.some(pipe => pipe.x + PIPE_WIDTH < 0) ? 1 : 0)
    }));
  };

  const jump = () => {
    if (!gameState.isPlaying || gameState.isGameOver) return;
    setGameState(prev => ({
      ...prev,
      birdVelocity: -8
    }));
  };

  // Game loop
  useEffect(() => {
    let animationFrameId;
    
    if (gameState.isPlaying && !gameState.isGameOver) {
      animationFrameId = requestAnimationFrame(updateGame);
    }

    return () => {
      if (animationFrameId) cancelAnimationFrame(animationFrameId);
    };
  }, [gameState.isPlaying, gameState.isGameOver]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">Flappy Bird</h1>
      
      <div 
        className="relative border-4 border-gray-500"
        style={{
          width: `${CANVAS_WIDTH}px`,
          height: `${CANVAS_HEIGHT}px`,
          backgroundColor: '#87CEEB',
          overflow: 'hidden'
        }}
      >
        {/* Pipes */}
        {gameState.pipes.map((pipe, index) => (
          <React.Fragment key={index}>
            <div 
              style={{
                position: 'absolute',
                left: `${pipe.x}px`,
                top: '0',
                width: `${PIPE_WIDTH}px`,
                height: `${pipe.topHeight}px`,
                backgroundColor: '#2ecc71'
              }}
            />
            <div 
              style={{
                position: 'absolute',
                left: `${pipe.x}px`,
                bottom: '0',
                width: `${PIPE_WIDTH}px`,
                height: `${pipe.bottomHeight}px`,
                backgroundColor: '#2ecc71'
              }}
            />
          </React.Fragment>
        ))}
        
        {/* Bird */}
        <div 
          style={{
            position: 'absolute',
            left: '20px',
            top: `${gameState.birdY}px`,
            width: `${BIRD_SIZE}px`,
            height: `${BIRD_SIZE}px`,
            borderRadius: '50%',
            backgroundColor: '#e74c3c'
          }}
        />
      </div>
      
      <div className="flex space-x-4 mt-4">
        {gameState.isGameOver && (
          <button 
            onClick={resetGame}
            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
          >
            Restart Game
          </button>
        )}
        
        {!gameState.isPlaying && !gameState.isGameOver && (
          <button 
            onClick={resetGame}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Start Game
          </button>
        )}
        
        {gameState.isPlaying && !gameState.isGameOver && (
          <button 
            onClick={jump}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Jump
          </button>
        )}
      </div>
      
      <div className="mt-4 text-xl font-semibold">
        Score: {gameState.score}
        {gameState.isGameOver && (
          <p className="text-red-500">Game Over!</p>
        )}
      </div>
    </div>
  );
};

export default FlappyBirdGame;
