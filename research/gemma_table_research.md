# Gemma 270M Table-of-N Workflow Research

This report is generated from the local experiment log.

## Fine-tuning environment check
- Time: 2026-03-23T23:05:00-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers import fails because the installed huggingface_hub is 1.4.1; datasets and peft are missing.

## Prompted-model fallback selected
- Time: 2026-03-23T23:05:00-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Model-only workflow implementation
- Time: 2026-03-23T23:05:00-07:00
- Category: implementation
- Status: success
- Summary: Implemented a side-by-side UI, benchmark harness, and research logging around original Gemma and a prompted Gemma path.
- Details:
  - ui_route: /gemma-table
  - report_path: /Users/mukesh/assistant2/research/gemma_table_research.md

## Fine-tuning environment check
- Time: 2026-03-23T23:07:23-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:07:23-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Fine-tuning environment check
- Time: 2026-03-23T23:07:27-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:07:27-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Side-by-side compare
- Time: 2026-03-23T23:07:28-07:00
- Category: inference
- Status: partial
- Summary: Compared original backend with prompted:ollama:gemma3:270m.
- Details:
  - query: what is 2+3
  - original_backend: ollama:gemma3:270m
  - original_success: False
  - original_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x0000000101163a84 ggml_print_backtrace + 276
1   ollama                              0x0000000101189840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]
  - new_backend: prompted:ollama:gemma3:270m
  - new_success: False
  - new_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x00000001056f7a84 ggml_print_backtrace + 276
1   ollama                              0x000000010571d840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]

## Side-by-side compare
- Time: 2026-03-23T23:07:28-07:00
- Category: inference
- Status: partial
- Summary: Compared original backend with prompted:ollama:gemma3:270m.
- Details:
  - query: what is 2+3
  - original_backend: ollama:gemma3:270m
  - original_success: False
  - original_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x0000000101163a84 ggml_print_backtrace + 276
1   ollama                              0x0000000101189840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]
  - new_backend: prompted:ollama:gemma3:270m
  - new_success: False
  - new_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x0000000102e4fa84 ggml_print_backtrace + 276
1   ollama                              0x0000000102e75840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]

## Side-by-side compare
- Time: 2026-03-23T23:07:28-07:00
- Category: inference
- Status: partial
- Summary: Compared original backend with prompted:ollama:gemma3:270m.
- Details:
  - query: table of 7
  - original_backend: ollama:gemma3:270m
  - original_success: False
  - original_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x0000000101163a84 ggml_print_backtrace + 276
1   ollama                              0x0000000101189840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]
  - new_backend: prompted:ollama:gemma3:270m
  - new_success: False
  - new_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x0000000102ef7a84 ggml_print_backtrace + 276
1   ollama                              0x0000000102f1d840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]

## Side-by-side compare
- Time: 2026-03-23T23:11:46-07:00
- Category: inference
- Status: success
- Summary: Compared original backend with prompted:ollama:gemma3:270m.
- Details:
  - query: table of 7
  - original_backend: ollama:gemma3:270m
  - original_success: True
  - original_error: None
  - new_backend: prompted:ollama:gemma3:270m
  - new_success: True
  - new_error: None

## Side-by-side compare
- Time: 2026-03-23T23:12:03-07:00
- Category: inference
- Status: success
- Summary: Compared original backend with prompted:ollama:gemma3:270m.
- Details:
  - query: table of 17
  - original_backend: ollama:gemma3:270m
  - original_success: True
  - original_error: None
  - new_backend: prompted:ollama:gemma3:270m
  - new_success: True
  - new_error: None

## Fine-tuning environment check
- Time: 2026-03-23T23:17:23-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:17:23-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Fine-tuning environment check
- Time: 2026-03-23T23:19:55-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:19:55-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Fine-tuning environment check
- Time: 2026-03-23T23:19:56-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:19:56-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Fine-tuning environment check
- Time: 2026-03-23T23:19:58-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:19:58-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Fine-tuning environment check
- Time: 2026-03-23T23:20:01-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:20:01-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Fine-tuning environment check
- Time: 2026-03-23T23:20:03-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:20:03-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Fine-tuning environment check
- Time: 2026-03-23T23:28:20-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:28:20-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Fine-tuning environment check
- Time: 2026-03-23T23:28:23-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:28:23-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Fine-tuning environment check
- Time: 2026-03-23T23:28:24-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:28:24-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Fine-tuning environment check
- Time: 2026-03-23T23:28:26-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:28:26-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Fine-tuning environment check
- Time: 2026-03-23T23:28:28-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:28:28-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Fine-tuning environment check
- Time: 2026-03-23T23:30:16-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:30:16-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Fine-tuning environment check
- Time: 2026-03-23T23:30:31-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:30:31-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Side-by-side compare
- Time: 2026-03-23T23:30:31-07:00
- Category: inference
- Status: partial
- Summary: Compared original backend with prompted:ollama:gemma3:270m.
- Details:
  - query: table of 17
  - original_backend: ollama:gemma3:270m
  - original_success: False
  - original_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x0000000101743a84 ggml_print_backtrace + 276
1   ollama                              0x0000000101769840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]
  - new_backend: prompted:ollama:gemma3:270m
  - new_success: False
  - new_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x000000010306fa84 ggml_print_backtrace + 276
1   ollama                              0x0000000103095840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]

## Baseline benchmark
- Time: 2026-03-23T23:31:09-07:00
- Category: evaluation
- Status: partial
- Summary: Measured original and new solution on table-of-N benchmark cases.
- Details:
  - total_cases: 13
  - original_exact_match_count: 0
  - new_exact_match_count: 0
  - original_exact_match_rate: 0.0
  - new_exact_match_rate: 0.0
  - fine_tune_needed: True
  - selected_solution: fine-tune-planned

## Workflow decision gate
- Time: 2026-03-23T23:31:09-07:00
- Category: workflow
- Status: success
- Summary: Evaluated whether fine-tuning is needed after the benchmark.
- Details:
  - fine_tune_needed: True
  - summary: {'total_cases': 13, 'original_exact_match_count': 0, 'new_exact_match_count': 0, 'original_exact_match_rate': 0.0, 'new_exact_match_rate': 0.0, 'fine_tune_needed': True, 'selected_solution': 'fine-tune-planned'}

## Fine-tuning environment check
- Time: 2026-03-23T23:35:48-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:35:48-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Synthetic SFT dataset generated
- Time: 2026-03-23T23:37:24-07:00
- Category: data
- Status: success
- Summary: Prepared supervised prompt/response pairs for table-of-N fine-tuning.
- Details:
  - dataset_path: research/data/gemma_table_sft.jsonl
  - train: 240
  - validation: 60

## Training device selected
- Time: 2026-03-23T23:37:24-07:00
- Category: training
- Status: success
- Summary: Selected training device for Gemma LoRA run.
- Details:
  - device: mps

## Fine-tuning environment check
- Time: 2026-03-23T23:37:43-07:00
- Category: environment
- Status: blocked
- Summary: Dependency stack is not ready for a Gemma LoRA run.
- Details:
  - reason: transformers -> ImportError: huggingface-hub>=0.34.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==1.4.1.
Try: `pip install transformers -U` or `pip install -e '.[dev]'` if you're working with git main; datasets -> ModuleNotFoundError: No module named 'datasets'; peft -> ModuleNotFoundError: No module named 'peft'

## Prompted-model fallback selected
- Time: 2026-03-23T23:37:43-07:00
- Category: strategy
- Status: success
- Summary: Using a static prompt-engineered Gemma path until fine-tuning is available.
- Details:
  - backend: prompted:ollama:gemma3:270m

## Synthetic SFT dataset generated
- Time: 2026-03-23T23:37:48-07:00
- Category: data
- Status: success
- Summary: Prepared supervised prompt/response pairs for table-of-N fine-tuning.
- Details:
  - dataset_path: research/data/gemma_table_sft.jsonl
  - train: 240
  - validation: 60

## Training device selected
- Time: 2026-03-23T23:37:48-07:00
- Category: training
- Status: success
- Summary: Selected training device for Gemma LoRA run.
- Details:
  - device: mps

## Gemma LoRA training completed
- Time: 2026-03-23T23:39:06-07:00
- Category: training
- Status: success
- Summary: Saved LoRA adapter and tokenizer for the table-of-N specialization.
- Details:
  - output_dir: research/models/gemma-table-lora-run1
  - model_id: google/gemma-3-270m-it

## Fine-tuned adapter selected
- Time: 2026-03-23T23:40:24-07:00
- Category: strategy
- Status: success
- Summary: Using the saved LoRA adapter as the new solution.
- Details:
  - backend: finetuned:gemma-table-lora-run1
  - adapter_dir: /Users/mukesh/assistant2/research/models/gemma-table-lora-run1

## Side-by-side compare
- Time: 2026-03-23T23:40:37-07:00
- Category: inference
- Status: success
- Summary: Compared original backend with finetuned:gemma-table-lora-run1.
- Details:
  - query: table of 17
  - original_backend: ollama:gemma3:270m
  - original_success: False
  - original_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x0000000103697a84 ggml_print_backtrace + 276
1   ollama                              0x00000001036bd840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]
  - new_backend: finetuned:gemma-table-lora-run1
  - new_success: True
  - new_error: None

## Side-by-side compare
- Time: 2026-03-23T23:42:20-07:00
- Category: inference
- Status: success
- Summary: Compared original backend with finetuned:gemma-table-lora-run1.
- Details:
  - query: table of 7
  - original_backend: ollama:gemma3:270m
  - original_success: True
  - original_error: None
  - new_backend: finetuned:gemma-table-lora-run1
  - new_success: True
  - new_error: None

## Side-by-side compare
- Time: 2026-03-23T23:43:00-07:00
- Category: inference
- Status: success
- Summary: Compared original backend with finetuned:gemma-table-lora-run1.
- Details:
  - query: table of 17
  - original_backend: ollama:gemma3:270m
  - original_success: True
  - original_error: None
  - new_backend: finetuned:gemma-table-lora-run1
  - new_success: True
  - new_error: None

## Side-by-side compare
- Time: 2026-03-23T23:43:32-07:00
- Category: inference
- Status: success
- Summary: Compared original backend with finetuned:gemma-table-lora-run1.
- Details:
  - query: what is 2 + 3

  - original_backend: ollama:gemma3:270m
  - original_success: True
  - original_error: None
  - new_backend: finetuned:gemma-table-lora-run1
  - new_success: True
  - new_error: None

## Fine-tuned adapter selected
- Time: 2026-03-23T23:44:42-07:00
- Category: strategy
- Status: success
- Summary: Using the saved LoRA adapter for table queries and the original model for everything else.
- Details:
  - backend: routed:finetuned:gemma-table-lora-run1
  - adapter_dir: /Users/mukesh/assistant2/research/models/gemma-table-lora-run1

## Side-by-side compare
- Time: 2026-03-23T23:44:57-07:00
- Category: inference
- Status: success
- Summary: Compared original backend with routed:finetuned:gemma-table-lora-run1.
- Details:
  - query: table of 17
  - original_backend: ollama:gemma3:270m
  - original_success: False
  - original_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x0000000104f63a84 ggml_print_backtrace + 276
1   ollama                              0x0000000104f89840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]
  - new_backend: finetuned:gemma-table-lora-run1
  - new_success: True
  - new_error: None

## Side-by-side compare
- Time: 2026-03-23T23:44:57-07:00
- Category: inference
- Status: partial
- Summary: Compared original backend with routed:finetuned:gemma-table-lora-run1.
- Details:
  - query: what is 2 + 3
  - original_backend: ollama:gemma3:270m
  - original_success: False
  - original_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x0000000104f63a84 ggml_print_backtrace + 276
1   ollama                              0x0000000104f89840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]
  - new_backend: routed:finetuned:gemma-table-lora-run1
  - new_success: False
  - new_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x000000010540fa84 ggml_print_backtrace + 276
1   ollama                              0x0000000105435840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]

## Fine-tuned adapter selected
- Time: 2026-03-23T23:50:28-07:00
- Category: strategy
- Status: success
- Summary: Using the saved LoRA adapter for table queries and the original model for everything else.
- Details:
  - backend: routed:finetuned:gemma-table-lora-run1
  - adapter_dir: /Users/mukesh/assistant2/research/models/gemma-table-lora-run1

## Side-by-side compare
- Time: 2026-03-23T23:50:28-07:00
- Category: inference
- Status: partial
- Summary: Compared original backend with routed:finetuned:gemma-table-lora-run1.
- Details:
  - query: What is 2 + 3?
  - original_backend: ollama:gemma3:270m
  - original_success: False
  - original_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x000000010111ba84 ggml_print_backtrace + 276
1   ollama                              0x0000000101141840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]
  - new_backend: routed:finetuned:gemma-table-lora-run1
  - new_success: False
  - new_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x0000000105187a84 ggml_print_backtrace + 276
1   ollama                              0x00000001051ad840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]

## Side-by-side compare
- Time: 2026-03-23T23:50:28-07:00
- Category: inference
- Status: partial
- Summary: Compared original backend with routed:finetuned:gemma-table-lora-run1.
- Details:
  - query: What color is the sky?
  - original_backend: ollama:gemma3:270m
  - original_success: False
  - original_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x000000010111ba84 ggml_print_backtrace + 276
1   ollama                              0x0000000101141840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]
  - new_backend: routed:finetuned:gemma-table-lora-run1
  - new_success: False
  - new_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x00000001012aba84 ggml_print_backtrace + 276
1   ollama                              0x00000001012d1840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]

## Side-by-side compare
- Time: 2026-03-23T23:50:28-07:00
- Category: inference
- Status: partial
- Summary: Compared original backend with routed:finetuned:gemma-table-lora-run1.
- Details:
  - query: How many days are in a week?
  - original_backend: ollama:gemma3:270m
  - original_success: False
  - original_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x000000010111ba84 ggml_print_backtrace + 276
1   ollama                              0x0000000101141840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]
  - new_backend: routed:finetuned:gemma-table-lora-run1
  - new_success: False
  - new_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x0000000101927a84 ggml_print_backtrace + 276
1   ollama                              0x000000010194d840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]

## Side-by-side compare
- Time: 2026-03-23T23:50:28-07:00
- Category: inference
- Status: partial
- Summary: Compared original backend with routed:finetuned:gemma-table-lora-run1.
- Details:
  - query: Which shape has 3 sides?
  - original_backend: ollama:gemma3:270m
  - original_success: False
  - original_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x000000010111ba84 ggml_print_backtrace + 276
1   ollama                              0x0000000101141840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]
  - new_backend: routed:finetuned:gemma-table-lora-run1
  - new_success: False
  - new_error: WARNING: Using native backtrace. Set GGML_BACKTRACE_LLDB for more info.
WARNING: GGML_BACKTRACE_LLDB may cause native MacOS Terminal.app to crash.
See: https://github.com/ggml-org/llama.cpp/pull/17869
0   ollama                              0x0000000105d8ba84 ggml_print_backtrace + 276
1   ollama                              0x0000000105db1840 ggml_critical_section_end + 52
2   libc++abi.dylib                     0x000000019c4e4c2c _ZSt11__terminatePFvvE + 16
3   libc++abi.dylib                     0x000000019c4e8394 __cxa_get_exception_ptr + 0
4   libc++abi.dylib                     0x0000000... [truncated]
