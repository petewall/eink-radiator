package pkg

type ImageConfig struct {
	Type     string                 `json:"type"`
	Name     string                 `json:"name,omitempty"`
	Duration string                 `json:"duration"`
	Params   map[string]interface{} `json:"params"`
}
