// Code generated by counterfeiter. DO NOT EDIT.
package internalfakes

import (
	"sync"

	"github.com/petewall/eink-radiator/v2/internal"
)

type FakeSession struct {
	OutputStub        func() ([]byte, error)
	outputMutex       sync.RWMutex
	outputArgsForCall []struct {
	}
	outputReturns struct {
		result1 []byte
		result2 error
	}
	outputReturnsOnCall map[int]struct {
		result1 []byte
		result2 error
	}
	RunStub        func() error
	runMutex       sync.RWMutex
	runArgsForCall []struct {
	}
	runReturns struct {
		result1 error
	}
	runReturnsOnCall map[int]struct {
		result1 error
	}
	invocations      map[string][][]interface{}
	invocationsMutex sync.RWMutex
}

func (fake *FakeSession) Output() ([]byte, error) {
	fake.outputMutex.Lock()
	ret, specificReturn := fake.outputReturnsOnCall[len(fake.outputArgsForCall)]
	fake.outputArgsForCall = append(fake.outputArgsForCall, struct {
	}{})
	stub := fake.OutputStub
	fakeReturns := fake.outputReturns
	fake.recordInvocation("Output", []interface{}{})
	fake.outputMutex.Unlock()
	if stub != nil {
		return stub()
	}
	if specificReturn {
		return ret.result1, ret.result2
	}
	return fakeReturns.result1, fakeReturns.result2
}

func (fake *FakeSession) OutputCallCount() int {
	fake.outputMutex.RLock()
	defer fake.outputMutex.RUnlock()
	return len(fake.outputArgsForCall)
}

func (fake *FakeSession) OutputCalls(stub func() ([]byte, error)) {
	fake.outputMutex.Lock()
	defer fake.outputMutex.Unlock()
	fake.OutputStub = stub
}

func (fake *FakeSession) OutputReturns(result1 []byte, result2 error) {
	fake.outputMutex.Lock()
	defer fake.outputMutex.Unlock()
	fake.OutputStub = nil
	fake.outputReturns = struct {
		result1 []byte
		result2 error
	}{result1, result2}
}

func (fake *FakeSession) OutputReturnsOnCall(i int, result1 []byte, result2 error) {
	fake.outputMutex.Lock()
	defer fake.outputMutex.Unlock()
	fake.OutputStub = nil
	if fake.outputReturnsOnCall == nil {
		fake.outputReturnsOnCall = make(map[int]struct {
			result1 []byte
			result2 error
		})
	}
	fake.outputReturnsOnCall[i] = struct {
		result1 []byte
		result2 error
	}{result1, result2}
}

func (fake *FakeSession) Run() error {
	fake.runMutex.Lock()
	ret, specificReturn := fake.runReturnsOnCall[len(fake.runArgsForCall)]
	fake.runArgsForCall = append(fake.runArgsForCall, struct {
	}{})
	stub := fake.RunStub
	fakeReturns := fake.runReturns
	fake.recordInvocation("Run", []interface{}{})
	fake.runMutex.Unlock()
	if stub != nil {
		return stub()
	}
	if specificReturn {
		return ret.result1
	}
	return fakeReturns.result1
}

func (fake *FakeSession) RunCallCount() int {
	fake.runMutex.RLock()
	defer fake.runMutex.RUnlock()
	return len(fake.runArgsForCall)
}

func (fake *FakeSession) RunCalls(stub func() error) {
	fake.runMutex.Lock()
	defer fake.runMutex.Unlock()
	fake.RunStub = stub
}

func (fake *FakeSession) RunReturns(result1 error) {
	fake.runMutex.Lock()
	defer fake.runMutex.Unlock()
	fake.RunStub = nil
	fake.runReturns = struct {
		result1 error
	}{result1}
}

func (fake *FakeSession) RunReturnsOnCall(i int, result1 error) {
	fake.runMutex.Lock()
	defer fake.runMutex.Unlock()
	fake.RunStub = nil
	if fake.runReturnsOnCall == nil {
		fake.runReturnsOnCall = make(map[int]struct {
			result1 error
		})
	}
	fake.runReturnsOnCall[i] = struct {
		result1 error
	}{result1}
}

func (fake *FakeSession) Invocations() map[string][][]interface{} {
	fake.invocationsMutex.RLock()
	defer fake.invocationsMutex.RUnlock()
	fake.outputMutex.RLock()
	defer fake.outputMutex.RUnlock()
	fake.runMutex.RLock()
	defer fake.runMutex.RUnlock()
	copiedInvocations := map[string][][]interface{}{}
	for key, value := range fake.invocations {
		copiedInvocations[key] = value
	}
	return copiedInvocations
}

func (fake *FakeSession) recordInvocation(key string, args []interface{}) {
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

var _ internal.Session = new(FakeSession)
