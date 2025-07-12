import React, { useState, useEffect } from "react"
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib"

const AnnotatedText = (props: any) => {
  // Get tokens and altPhrases from Streamlit props
  const { tokens: initialTokens, altPhrases: initialAltPhrases } = props.args

  const [tokens, setTokens] = useState(initialTokens)
  const [altPhrases] = useState(initialAltPhrases)
  const [selectedChunkIndex, setSelectedChunkIndex] = useState(0)

  // Debug logging
  console.log("AnnotatedText props:", props.args)
  console.log("Initial tokens:", initialTokens)
  console.log("Initial altPhrases:", initialAltPhrases)

  // Simple test render
  console.log("Component is rendering!")

  // Set iframe height
  useEffect(() => {
    Streamlit.setFrameHeight(400) // Set a fixed height
  }, [])

  const handleAlternativeClick = (newWord: string) => {
    const newTokens = tokens.map((token: any, i: number) =>
      i === selectedChunkIndex ? [newWord, token[1]] : token
    )
    setTokens(newTokens)
    // Advance to next chunk, or stay on current if it's the last one
    if (selectedChunkIndex < tokens.length - 1) {
      setSelectedChunkIndex(selectedChunkIndex + 1)
    }
    setTimeout(() => {
      Streamlit.setFrameHeight(document.body.scrollHeight)
    }, 0)
  }

  const handleChunkClick = (index: number) => {
    setSelectedChunkIndex(selectedChunkIndex === index ? -1 : index)
    setTimeout(() => {
      Streamlit.setFrameHeight(document.body.scrollHeight)
    }, 0)
  }

  const renderAlternatives = () => {
    if (selectedChunkIndex === null) return null
    const chunkText = tokens[selectedChunkIndex][0]
    if (!altPhrases || !altPhrases[chunkText]) return null
    return (
      <div
        style={{
          marginTop: "0.5rem",
          padding: "8px",
          backgroundColor: "#f0f7ff",
          borderRadius: "5px",
        }}
      >
        <div style={{ fontWeight: "bold", marginBottom: "4px" }}>
          Alternative phrases:
        </div>
        {altPhrases[chunkText].map((alt: string, i: number) => (
          <div
            key={i}
            onClick={() => handleAlternativeClick(alt)}
            style={{
              padding: "4px 8px",
              margin: "2px 0",
              backgroundColor: "#ffffff",
              borderRadius: "3px",
              cursor: "pointer",
              transition: "background-color 0.2s",
            }}
          >
            {alt}
          </div>
        ))}
      </div>
    )
  }

  try {
    return (
      <div
        style={{
          height: "auto",
          padding: "20px",
          width: "100%", // Bright red background
          borderRadius: "8px", // Blue border
          margin: "10px 0",
        }}
      >
        {tokens && tokens.length > 0 ? (
          <p
            style={{
              fontSize: "18px",
              lineHeight: "2.0",
              margin: "0 0 20px 0",
            }}
          >
            {tokens.map((token: any, i: number) => {
              if (Array.isArray(token)) {
                const [word, label] = token
                const isSelected = selectedChunkIndex === i
                const bgColor = isSelected ? "#ffe066" : "#d0e6f7" // yellow if selected, blue otherwise
                return (
                  <span
                    key={i}
                    className="clickable"
                    onClick={() => handleChunkClick(i)}
                    style={{
                      backgroundColor: bgColor,
                      padding: "4px 8px",
                      margin: "0 4px",
                      borderRadius: "5px",
                      cursor: "pointer",
                      fontWeight: isSelected ? "bold" : "normal",
                      transition: "background-color 0.2s",
                    }}
                  >
                    {word}
                  </span>
                )
              }
              return <span key={i}>{token}</span>
            })}
          </p>
        ) : (
          <p>No tokens available</p>
        )}
        {renderAlternatives()}
        <style>
          {`
            .clickable:hover {
              background-color: #a3d0f0 !important;
            }
          `}
        </style>
      </div>
    )
  } catch (error) {
    console.error("Error in AnnotatedText component:", error)
    return <div>Error: {(error as Error).message}</div>
  }
}

export default withStreamlitConnection(AnnotatedText)
