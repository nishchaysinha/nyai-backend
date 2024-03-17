from langchain.prompts import PromptTemplate

def init_prompt(event_data_json):
    initial_prompt_template = PromptTemplate.from_template(
        """
        You are an HR manager at a company. You have been asked to investigate a recent event that has occurred at your organization. You have been given the following data about the event:
        
        {event_data}

        Based on this data, you have to provide a valid judgement about the event along with the reasons for your judgement. and a confidence score for your judgement.

        return a json object with the following keys:
        - judgement: True or False(True if victim is right, False if accused is right)
        - reasons: a string representing the reasons for your judgement
        """
    )

    x = PromptTemplate.format(initial_prompt_template,event_data=event_data_json)
    # convert prompt to string
    return x

def title_prompt(event_report_text):
    initial_prompt_template = PromptTemplate.from_template(
        """
        The following is information about a recent event that has occurred at your organization.
        
        {event_report}

        Based on this data, generate a short title for the event.
        """
    )

    x = PromptTemplate.format(initial_prompt_template,event_report=event_report_text)
    # convert prompt to string

    return x

def short_desc_prompt(event_report_text):
    initial_prompt_template = PromptTemplate.from_template(
        """
        The following is information about a recent event that has occurred at your organization.
        
        {event_report}

        Based on this data, generate a short description for the event.
        """
    )

    x = PromptTemplate.format(initial_prompt_template,event_report=event_report_text)
    # convert prompt to string

    return x