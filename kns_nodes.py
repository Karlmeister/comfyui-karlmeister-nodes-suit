from datetime import datetime, timezone
import comfy
import impact.core as core

# Monkey patch schedulers
SCHEDULERS = comfy.samplers.KSampler.SCHEDULERS + ["AYS SD1", "AYS SDXL", "AYS SVD", "GITS"]
EASYUSE_SCHEDULERS = comfy.samplers.KSampler.SCHEDULERS + ['align_your_steps', 'gits']

class KNS_SeedFilenameGenerator:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "filename_prefix": ("STRING", {"default":"ComfyUI"}),
                "time_format": ("STRING", {"default": "%Y%m%d_%H%M%S"}),
                "delimiter": ("STRING", {"default":"_"}),
            },
            "optional":
            {
                "output_path": ("STRING", {"default":"ComfyUI"})
            }
        }
 
    RETURN_TYPES = ("INT", "STRING", "STRING")
    RETURN_NAMES = ("seed", "filename", "output_path")
 
    FUNCTION = "generate"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "Karlmeister Nodes"
 
    def generate(self, seed, filename_prefix, output_path, time_format, delimiter):
        timestamp = datetime.now().strftime(time_format)
        filename = delimiter.join((filename_prefix, timestamp, str(seed)))
        return (seed, filename, output_path)
     
class KNS_KSamplerConfigSelector:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
            },
            "optional":
            {
                "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
                "cfg": ("FLOAT", {"default": 7.0, "min": 0.0, "max": 100.0}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS,),
                "scheduler": (SCHEDULERS,),
                "impact_scheduler": (core.SCHEDULERS,),
                "easy_use_scheduler": (EASYUSE_SCHEDULERS,),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01})
            }
        }
 
    RETURN_TYPES = ("INT", "FLOAT", comfy.samplers.KSampler.SAMPLERS, SCHEDULERS, core.SCHEDULERS, EASYUSE_SCHEDULERS, "FLOAT", "KSamplerConfigTuple",)
    RETURN_NAMES = ("steps", "cfg", "sampler_name", "scheduler", "impact_scheduler", "easy_use_scheduler", "denoise", "ksamplerconfig",)
 
    FUNCTION = "generate"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "Karlmeister Nodes"
 
    def generate(self, steps, cfg, sampler_name, scheduler, impact_scheduler, easy_use_scheduler, denoise):
        ksamplerconfig = (steps, cfg, sampler_name, scheduler, impact_scheduler, easy_use_scheduler, denoise)
        return (steps, cfg, sampler_name, scheduler, impact_scheduler, easy_use_scheduler, denoise, ksamplerconfig,)
        
class KNS_KSamplerConfigSelector_Tuple:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
            },
            "optional":
            {
                "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
                "cfg": ("FLOAT", {"default": 7.0, "min": 0.0, "max": 100.0}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS,),
                "scheduler": (SCHEDULERS,),
                "impact_scheduler": (core.SCHEDULERS,),
                "easy_use_scheduler": (EASYUSE_SCHEDULERS,),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01})
            }
        }
 
    RETURN_TYPES = ("KSamplerConfigTuple",)
    RETURN_NAMES = ("ksamplerconfig",)
 
    FUNCTION = "generate"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "Karlmeister Nodes"
 
    def generate(self, steps, cfg, sampler_name, scheduler, impact_scheduler, easy_use_scheduler, denoise):
        return ((steps, cfg, sampler_name, scheduler, impact_scheduler, easy_use_scheduler, denoise),)
        
class KNS_KSamplerConfigUnpack:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"ksamplerconfig": ("KSamplerConfigTuple",)},}
        
    RETURN_TYPES = ("INT", "FLOAT", comfy.samplers.KSampler.SAMPLERS, SCHEDULERS, core.SCHEDULERS, EASYUSE_SCHEDULERS, "FLOAT",)
    RETURN_NAMES = ("steps", "cfg", "sampler_name", "scheduler", "impact_scheduler", "easy_use_scheduler", "denoise",)
    FUNCTION = "unpack_KSamplerConfigTuple"
    CATEGORY = "Karlmeister Nodes"
    
    def unpack_KSamplerConfigTuple(self, ksamplerconfig):
        return (ksamplerconfig[0], ksamplerconfig[1], ksamplerconfig[2], ksamplerconfig[3],
                ksamplerconfig[4], ksamplerconfig[5], ksamplerconfig[6],)
    
class KNS_TextConcatenator:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "delimiter": ("STRING", {"default": ", "}),
                "clean_whitespace": (["true", "false"],),
            },
            "optional": {
                "text_a": ("STRING", {"forceInput": True}),
                "text_b": ("STRING", {"forceInput": True}),
                "text_c": ("STRING", {"forceInput": True}),
                "text_d": ("STRING", {"forceInput": True}),
                "text_e": ("STRING", {"forceInput": True}),
                "text_f": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"

    CATEGORY = "Karlmeister Nodes"

    def generate(self, delimiter, clean_whitespace, **kwargs):
        text_inputs = []

        # Handle special case where delimiter is "\n" (literal newline).
        if delimiter in ("\n", "\\n"):
            delimiter = "\n"

        # Iterate over the received inputs in sorted order.
        for k in sorted(kwargs.keys()):
            v = kwargs[k]

            # Only process string input ports.
            if isinstance(v, str):
                if clean_whitespace == "true":
                    # Remove leading and trailing whitespace around this input.
                    v = v.strip()

                # Only use this input if it's a non-empty string, since it
                # never makes sense to concatenate totally empty inputs.
                # NOTE: If whitespace cleanup is disabled, inputs containing
                # 100% whitespace will be treated as if it's a non-empty input.
                if v != "":
                    text_inputs.append(v)

        # Merge the inputs. Will always generate an output, even if empty.
        merged_text = delimiter.join(text_inputs)
        
        return (merged_text,)
        
# wildcard trick is taken from pythongossss's
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

# Splits the input string
class KNS_SplitString:

    @classmethod
    def INPUT_TYPES(s):  
    
        return {"required": {
                "text": ("STRING", {"multiline": False, "default": "text"}),
            },
            "optional": {
                "delimiter": ("STRING", {"multiline": False, "default": ","}),
            }            
        }

    RETURN_TYPES = (any_type, any_type, any_type, any_type, )
    RETURN_NAMES = ("string_1", "string_2", "string_3", "string_4", )    
    FUNCTION = "split"
    CATEGORY = "Karlmeister Nodes"

    def split(self, text, delimiter=""):

        # Split the text string
        parts = text.split(delimiter)
        strings = [part.strip() for part in parts[:4]]
        string_1, string_2, string_3, string_4 = strings + [""] * (4 - len(strings))            

        return (string_1, string_2, string_3, string_4, )

# Returns the first if it isn't None. Otherwise, returns the second one.
class KNS_A_IfNotNone:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "input_a": (any_type,),
                "input_b": (any_type,),
            }
        }

    RETURN_TYPES = (any_type, "BOOLEAN",)
    RETURN_NAMES = ("output", "is_input_a_none",)
    FUNCTION = "checkNone"

    CATEGORY = "Karlmeister Nodes"

    def checkNone(self, input_a=None, input_b=None):
        result = input_a
        is_a_none = False
        
        if input_a is None:
            result = input_b
            is_a_none = True
        
        return (result, is_a_none,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "SeedFilenameGenerator": KNS_SeedFilenameGenerator,
    "KSamplerConfigSelector": KNS_KSamplerConfigSelector,
    "KSamplerConfigSelector_Tuple": KNS_KSamplerConfigSelector_Tuple,
    "KSamplerConfigUnpack": KNS_KSamplerConfigUnpack,
    "TextConcatenator": KNS_TextConcatenator,
    "A_IfNotNone": KNS_A_IfNotNone,
    "SplitString": KNS_SplitString
}
 
# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "SeedFilenameGenerator": "Seed with Filename Generator",
    "KSamplerConfigSelector": "KSampler Config Selector",
    "KSamplerConfigSelector_Tuple": "KSampler Config Selector With Tuple Output",
    "KSamplerConfigUnpack": "KSampler Config Tuple",
    "TextConcatenator": "Text Concatenator",
    "A_IfNotNone": "A If Not None.",
    "SplitString": "Split a string."
}