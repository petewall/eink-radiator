package pkg

type ScreenSize struct {
	Height int `json:"height"`
	Width  int `json:"width"`
}

type ScreenConfig struct {
	Size    ScreenSize `json:"size"`
	Palette []string   `json:"palette"`
}
