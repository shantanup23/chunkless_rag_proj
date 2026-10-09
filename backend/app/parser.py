from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling_core.types.doc import PictureItem
import os

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extracted_assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

def parse_pdf(pdf_path: str, doc_id: str) -> str:
    # Set up pipeline options to extract images
    pipeline_options = PdfPipelineOptions()
    pipeline_options.generate_picture_images = True
    
    # Configure document converter
    doc_converter = DocumentConverter(
        allowed_formats=[InputFormat.PDF],
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    
    # Convert the document
    conv_res = doc_converter.convert(pdf_path)
    
    # Save the extracted images to the assets directory
    for element, _level in conv_res.document.iterate_items():
        if isinstance(element, PictureItem):
            try:
                img = element.get_image(conv_res.document)
                if img:
                    ref_id = element.self_ref.split('/')[-1] if hasattr(element, 'self_ref') else str(id(element))
                    image_path = os.path.join(ASSETS_DIR, f"{doc_id}_{ref_id}.png")
                    img.save(image_path, "PNG")
            except Exception as e:
                print(f"Failed to extract image: {e}")
            
    # Export to markdown
    return conv_res.document.export_to_markdown()
