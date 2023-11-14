from django.views.generic import TemplateView

def ScrollSpyTemplateView(template_name:str,
                          target_id:str = 'ScrollSpyDataTarget'):
    return TemplateView.as_view(
                template_name = template_name,
                extra_context = {
                    'ScrollSpyDataTargetID': target_id
                },)