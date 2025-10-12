import React, { useState, useRef, useEffect } from 'react';
import { 
  Play, 
  Pause, 
  SkipForward, 
  SkipBack,
  Volume2, 
  VolumeX,
  Maximize,
  Minimize,
  RotateCcw
} from 'lucide-react';
import './MediaPlayer.css';

const MediaPlayer = ({ 
  session, 
  isPlaying, 
  onPlayPause, 
  onProgressUpdate,
  onSessionComplete,
  className = '' 
}) => {
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(0.7);
  const [isMuted, setIsMuted] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const mediaRef = useRef(null);
  const progressRef = useRef(null);
  const volumeRef = useRef(null);
  const containerRef = useRef(null);

  // Initialize media when session changes
  useEffect(() => {
    if (session && mediaRef.current) {
      setIsLoading(true);
      setCurrentTime(0);
      
      const media = mediaRef.current;
      media.volume = volume;
      
      const handleLoadedMetadata = () => {
        setDuration(media.duration);
        setIsLoading(false);
      };
      
      const handleLoadStart = () => {
        setIsLoading(true);
      };
      
      const handleCanPlay = () => {
        setIsLoading(false);
      };
      
      media.addEventListener('loadedmetadata', handleLoadedMetadata);
      media.addEventListener('loadstart', handleLoadStart);
      media.addEventListener('canplay', handleCanPlay);
      
      return () => {
        media.removeEventListener('loadedmetadata', handleLoadedMetadata);
        media.removeEventListener('loadstart', handleLoadStart);
        media.removeEventListener('canplay', handleCanPlay);
      };
    }
  }, [session, volume]);

  // Handle play/pause state changes
  useEffect(() => {
    if (mediaRef.current) {
      if (isPlaying) {
        mediaRef.current.play().catch(console.error);
      } else {
        mediaRef.current.pause();
      }
    }
  }, [isPlaying]);

  // Update progress and handle session completion
  useEffect(() => {
    const media = mediaRef.current;
    if (!media) return;

    const handleTimeUpdate = () => {
      const current = media.currentTime;
      setCurrentTime(current);
      
      // Update progress in backend
      if (onProgressUpdate && session) {
        onProgressUpdate(session.id, Math.floor(current));
      }
      
      // Check if session is near completion (95% completed)
      if (duration > 0 && current / duration > 0.95 && onSessionComplete) {
        onSessionComplete(session.id);
      }
    };

    const handleEnded = () => {
      setCurrentTime(duration);
      if (onSessionComplete && session) {
        onSessionComplete(session.id);
      }
    };

    media.addEventListener('timeupdate', handleTimeUpdate);
    media.addEventListener('ended', handleEnded);

    return () => {
      media.removeEventListener('timeupdate', handleTimeUpdate);
      media.removeEventListener('ended', handleEnded);
    };
  }, [duration, onProgressUpdate, onSessionComplete, session]);

  const handleProgressClick = (e) => {
    if (!progressRef.current || !mediaRef.current || !duration) return;
    
    const rect = progressRef.current.getBoundingClientRect();
    const pos = (e.clientX - rect.left) / rect.width;
    const newTime = pos * duration;
    
    mediaRef.current.currentTime = newTime;
    setCurrentTime(newTime);
  };

  const handleVolumeClick = (e) => {
    if (!volumeRef.current) return;
    
    const rect = volumeRef.current.getBoundingClientRect();
    const pos = (e.clientX - rect.left) / rect.width;
    const newVolume = Math.max(0, Math.min(1, pos));
    
    setVolume(newVolume);
    setIsMuted(false);
    if (mediaRef.current) {
      mediaRef.current.volume = newVolume;
    }
  };

  const toggleMute = () => {
    if (mediaRef.current) {
      if (isMuted) {
        mediaRef.current.volume = volume;
        setIsMuted(false);
      } else {
        mediaRef.current.volume = 0;
        setIsMuted(true);
      }
    }
  };

  const skip = (seconds) => {
    if (mediaRef.current && duration) {
      const newTime = Math.max(0, Math.min(duration, currentTime + seconds));
      mediaRef.current.currentTime = newTime;
      setCurrentTime(newTime);
    }
  };

  const restart = () => {
    if (mediaRef.current) {
      mediaRef.current.currentTime = 0;
      setCurrentTime(0);
    }
  };

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      containerRef.current.requestFullscreen().then(() => {
        setIsFullscreen(true);
      });
    } else {
      document.exitFullscreen().then(() => {
        setIsFullscreen(false);
      });
    }
  };

  const formatTime = (seconds) => {
    if (!seconds || isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (!session) {
    return (
      <div className={`media-player ${className}`}>
        <div className="no-session">
          <p>Select a session to begin your mindfulness journey</p>
        </div>
      </div>
    );
  }

  const progressPercentage = duration ? (currentTime / duration) * 100 : 0;
  const volumePercentage = isMuted ? 0 : volume * 100;

  return (
    <div ref={containerRef} className={`media-player ${className} ${isFullscreen ? 'fullscreen' : ''}`}>
      {/* Media Element */}
      {session.content_type === 'video' && session.video ? (
        <video
          ref={mediaRef}
          src={session.video}
          poster={session.image}
          className="media-element video"
          preload="metadata"
        />
      ) : (
        <audio
          ref={mediaRef}
          src={session.audio}
          className="media-element audio"
          preload="metadata"
        />
      )}

      {/* Session Info */}
      <div className="session-info">
        <div className="session-image">
          <img src={session.image} alt={session.title} />
          {isLoading && (
            <div className="loading-overlay">
              <div className="spinner"></div>
            </div>
          )}
        </div>
        <div className="session-details">
          <h3 className="session-title">{session.title}</h3>
          <p className="session-instructor">by {session.instructor}</p>
          <div className="session-meta">
            <span className="category">{session.category}</span>
            <span className="difficulty">{session.difficulty}</span>
            <span className="rating">★ {session.rating}</span>
          </div>
        </div>
      </div>

      {/* Player Controls */}
      <div className="player-controls">
        <div className="primary-controls">
          <button 
            className="control-btn restart-btn" 
            onClick={restart}
            title="Restart"
          >
            <RotateCcw size={18} />
          </button>
          
          <button 
            className="control-btn skip-btn" 
            onClick={() => skip(-10)}
            title="Skip back 10s"
          >
            <SkipBack size={18} />
          </button>
          
          <button 
            className="play-pause-btn"
            onClick={onPlayPause}
            disabled={isLoading}
            title={isPlaying ? 'Pause' : 'Play'}
          >
            {isLoading ? (
              <div className="spinner small"></div>
            ) : isPlaying ? (
              <Pause size={24} />
            ) : (
              <Play size={24} />
            )}
          </button>
          
          <button 
            className="control-btn skip-btn" 
            onClick={() => skip(10)}
            title="Skip forward 10s"
          >
            <SkipForward size={18} />
          </button>
          
          <button 
            className="control-btn fullscreen-btn" 
            onClick={toggleFullscreen}
            title={isFullscreen ? 'Exit fullscreen' : 'Fullscreen'}
          >
            {isFullscreen ? <Minimize size={18} /> : <Maximize size={18} />}
          </button>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="progress-section">
        <span className="time current-time">{formatTime(currentTime)}</span>
        <div 
          ref={progressRef}
          className="progress-bar"
          onClick={handleProgressClick}
          title={`${Math.round(progressPercentage)}% complete`}
        >
          <div 
            className="progress-fill" 
            style={{ width: `${progressPercentage}%` }}
          />
          <div 
            className="progress-handle"
            style={{ left: `${progressPercentage}%` }}
          />
        </div>
        <span className="time total-time">{formatTime(duration)}</span>
      </div>

      {/* Volume Control */}
      <div className="volume-section">
        <button 
          className="volume-btn"
          onClick={toggleMute}
          title={isMuted ? 'Unmute' : 'Mute'}
        >
          {isMuted || volume === 0 ? <VolumeX size={20} /> : <Volume2 size={20} />}
        </button>
        
        <div 
          ref={volumeRef}
          className="volume-bar"
          onClick={handleVolumeClick}
          title={`Volume: ${Math.round(volumePercentage)}%`}
        >
          <div 
            className="volume-fill" 
            style={{ width: `${volumePercentage}%` }}
          />
          <div 
            className="volume-handle"
            style={{ left: `${volumePercentage}%` }}
          />
        </div>
      </div>
    </div>
  );
};

export default MediaPlayer;