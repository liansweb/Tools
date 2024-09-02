from obsei.source.google_news_source import GoogleNewsConfig, GoogleNewsSource

# initialize Google News source config
source_config = GoogleNewsConfig(
   query='bitcoin',
   max_results=5,
   # To fetch full article text enable `fetch_article` flag
   # By default google news gives title and highlight
   fetch_article=True,
   # proxy='http://127.0.0.1:8080'
)

# initialize Google News retriever
source = GoogleNewsSource()



from obsei.analyzer.classification_analyzer import ClassificationAnalyzerConfig, ZeroShotClassificationAnalyzer

# initialize classification analyzer config
# It can also detect sentiments if "positive" and "negative" labels are added.
analyzer_config=ClassificationAnalyzerConfig(
   labels=["service", "delay", "performance"],
)

# initialize classification analyzer
# For supported models refer https://huggingface.co/models?filter=zero-shot-classification
text_analyzer = ZeroShotClassificationAnalyzer(
   model_name_or_path="typeform/mobilebert-uncased-mnli",
   device="auto"
)

from obsei.sink.logger_sink import LoggerSink, LoggerSinkConfig
import logging
import sys

logger = logging.getLogger("Obsei")
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# initialize logger sink config
sink_config = LoggerSinkConfig(
   logger=logger,
   level=logging.INFO
)

# initialize logger sink
sink = LoggerSink()



# Uncomment if you want logger
# import logging
# import sys
# logger = logging.getLogger(__name__)
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# This will fetch information from configured source ie twitter, app store etc
source_response_list = source.lookup(source_config)


# Uncomment if you want to log source response
# for idx, source_response in enumerate(source_response_list):
#     logger.info(f"source_response#'{idx}'='{source_response.__dict__}'")

# This will execute analyzer (Sentiment, classification etc) on source data with provided analyzer_config
analyzer_response_list = text_analyzer.analyze_input(
    source_response_list=source_response_list,
    analyzer_config=analyzer_config
)

# Uncomment if you want to log analyzer response
# for idx, an_response in enumerate(analyzer_response_list):
#    logger.info(f"analyzer_response#'{idx}'='{an_response.__dict__}'")

# Analyzer output added to segmented_data
# Uncomment to log it
# for idx, an_response in enumerate(analyzer_response_list):
#    logger.info(f"analyzed_data#'{idx}'='{an_response.segmented_data.__dict__}'")

# This will send analyzed output to configure sink ie Slack, Zendesk etc
sink_response_list = sink.send_data(analyzer_response_list, sink_config)

# Uncomment if you want to log sink response
# for sink_response in sink_response_list:
#     if sink_response is not None:
#         logger.info(f"sink_response='{sink_response}'")

def main():
    pass


if __name__ == '__main__':
    main()