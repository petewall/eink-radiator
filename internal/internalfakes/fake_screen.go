// Code generated by counterfeiter. DO NOT EDIT.
package internalfakes

import (
	"sync"

	"github.com/petewall/eink-radiator/v2/internal"
)

type FakeScreen struct {
	GetPaletteStub        func() []string
	getPaletteMutex       sync.RWMutex
	getPaletteArgsForCall []struct {
	}
	getPaletteReturns struct {
		result1 []string
	}
	getPaletteReturnsOnCall map[int]struct {
		result1 []string
	}
	GetSizeStub        func() *internal.ScreenSize
	getSizeMutex       sync.RWMutex
	getSizeArgsForCall []struct {
	}
	getSizeReturns struct {
		result1 *internal.ScreenSize
	}
	getSizeReturnsOnCall map[int]struct {
		result1 *internal.ScreenSize
	}
	SetImageStub        func(string) error
	setImageMutex       sync.RWMutex
	setImageArgsForCall []struct {
		arg1 string
	}
	setImageReturns struct {
		result1 error
	}
	setImageReturnsOnCall map[int]struct {
		result1 error
	}
	invocations      map[string][][]interface{}
	invocationsMutex sync.RWMutex
}

func (fake *FakeScreen) GetPalette() []string {
	fake.getPaletteMutex.Lock()
	ret, specificReturn := fake.getPaletteReturnsOnCall[len(fake.getPaletteArgsForCall)]
	fake.getPaletteArgsForCall = append(fake.getPaletteArgsForCall, struct {
	}{})
	stub := fake.GetPaletteStub
	fakeReturns := fake.getPaletteReturns
	fake.recordInvocation("GetPalette", []interface{}{})
	fake.getPaletteMutex.Unlock()
	if stub != nil {
		return stub()
	}
	if specificReturn {
		return ret.result1
	}
	return fakeReturns.result1
}

func (fake *FakeScreen) GetPaletteCallCount() int {
	fake.getPaletteMutex.RLock()
	defer fake.getPaletteMutex.RUnlock()
	return len(fake.getPaletteArgsForCall)
}

func (fake *FakeScreen) GetPaletteCalls(stub func() []string) {
	fake.getPaletteMutex.Lock()
	defer fake.getPaletteMutex.Unlock()
	fake.GetPaletteStub = stub
}

func (fake *FakeScreen) GetPaletteReturns(result1 []string) {
	fake.getPaletteMutex.Lock()
	defer fake.getPaletteMutex.Unlock()
	fake.GetPaletteStub = nil
	fake.getPaletteReturns = struct {
		result1 []string
	}{result1}
}

func (fake *FakeScreen) GetPaletteReturnsOnCall(i int, result1 []string) {
	fake.getPaletteMutex.Lock()
	defer fake.getPaletteMutex.Unlock()
	fake.GetPaletteStub = nil
	if fake.getPaletteReturnsOnCall == nil {
		fake.getPaletteReturnsOnCall = make(map[int]struct {
			result1 []string
		})
	}
	fake.getPaletteReturnsOnCall[i] = struct {
		result1 []string
	}{result1}
}

func (fake *FakeScreen) GetSize() *internal.ScreenSize {
	fake.getSizeMutex.Lock()
	ret, specificReturn := fake.getSizeReturnsOnCall[len(fake.getSizeArgsForCall)]
	fake.getSizeArgsForCall = append(fake.getSizeArgsForCall, struct {
	}{})
	stub := fake.GetSizeStub
	fakeReturns := fake.getSizeReturns
	fake.recordInvocation("GetSize", []interface{}{})
	fake.getSizeMutex.Unlock()
	if stub != nil {
		return stub()
	}
	if specificReturn {
		return ret.result1
	}
	return fakeReturns.result1
}

func (fake *FakeScreen) GetSizeCallCount() int {
	fake.getSizeMutex.RLock()
	defer fake.getSizeMutex.RUnlock()
	return len(fake.getSizeArgsForCall)
}

func (fake *FakeScreen) GetSizeCalls(stub func() *internal.ScreenSize) {
	fake.getSizeMutex.Lock()
	defer fake.getSizeMutex.Unlock()
	fake.GetSizeStub = stub
}

func (fake *FakeScreen) GetSizeReturns(result1 *internal.ScreenSize) {
	fake.getSizeMutex.Lock()
	defer fake.getSizeMutex.Unlock()
	fake.GetSizeStub = nil
	fake.getSizeReturns = struct {
		result1 *internal.ScreenSize
	}{result1}
}

func (fake *FakeScreen) GetSizeReturnsOnCall(i int, result1 *internal.ScreenSize) {
	fake.getSizeMutex.Lock()
	defer fake.getSizeMutex.Unlock()
	fake.GetSizeStub = nil
	if fake.getSizeReturnsOnCall == nil {
		fake.getSizeReturnsOnCall = make(map[int]struct {
			result1 *internal.ScreenSize
		})
	}
	fake.getSizeReturnsOnCall[i] = struct {
		result1 *internal.ScreenSize
	}{result1}
}

func (fake *FakeScreen) SetImage(arg1 string) error {
	fake.setImageMutex.Lock()
	ret, specificReturn := fake.setImageReturnsOnCall[len(fake.setImageArgsForCall)]
	fake.setImageArgsForCall = append(fake.setImageArgsForCall, struct {
		arg1 string
	}{arg1})
	stub := fake.SetImageStub
	fakeReturns := fake.setImageReturns
	fake.recordInvocation("SetImage", []interface{}{arg1})
	fake.setImageMutex.Unlock()
	if stub != nil {
		return stub(arg1)
	}
	if specificReturn {
		return ret.result1
	}
	return fakeReturns.result1
}

func (fake *FakeScreen) SetImageCallCount() int {
	fake.setImageMutex.RLock()
	defer fake.setImageMutex.RUnlock()
	return len(fake.setImageArgsForCall)
}

func (fake *FakeScreen) SetImageCalls(stub func(string) error) {
	fake.setImageMutex.Lock()
	defer fake.setImageMutex.Unlock()
	fake.SetImageStub = stub
}

func (fake *FakeScreen) SetImageArgsForCall(i int) string {
	fake.setImageMutex.RLock()
	defer fake.setImageMutex.RUnlock()
	argsForCall := fake.setImageArgsForCall[i]
	return argsForCall.arg1
}

func (fake *FakeScreen) SetImageReturns(result1 error) {
	fake.setImageMutex.Lock()
	defer fake.setImageMutex.Unlock()
	fake.SetImageStub = nil
	fake.setImageReturns = struct {
		result1 error
	}{result1}
}

func (fake *FakeScreen) SetImageReturnsOnCall(i int, result1 error) {
	fake.setImageMutex.Lock()
	defer fake.setImageMutex.Unlock()
	fake.SetImageStub = nil
	if fake.setImageReturnsOnCall == nil {
		fake.setImageReturnsOnCall = make(map[int]struct {
			result1 error
		})
	}
	fake.setImageReturnsOnCall[i] = struct {
		result1 error
	}{result1}
}

func (fake *FakeScreen) Invocations() map[string][][]interface{} {
	fake.invocationsMutex.RLock()
	defer fake.invocationsMutex.RUnlock()
	fake.getPaletteMutex.RLock()
	defer fake.getPaletteMutex.RUnlock()
	fake.getSizeMutex.RLock()
	defer fake.getSizeMutex.RUnlock()
	fake.setImageMutex.RLock()
	defer fake.setImageMutex.RUnlock()
	copiedInvocations := map[string][][]interface{}{}
	for key, value := range fake.invocations {
		copiedInvocations[key] = value
	}
	return copiedInvocations
}

func (fake *FakeScreen) recordInvocation(key string, args []interface{}) {
	fake.invocationsMutex.Lock()
	defer fake.invocationsMutex.Unlock()
	if fake.invocations == nil {
		fake.invocations = map[string][][]interface{}{}
	}
	if fake.invocations[key] == nil {
		fake.invocations[key] = [][]interface{}{}
	}
	fake.invocations[key] = append(fake.invocations[key], args)
}

var _ internal.Screen = new(FakeScreen)
