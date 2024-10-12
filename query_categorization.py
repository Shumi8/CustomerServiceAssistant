def gpt_response_generator(prompt, user_email, ticket_id):
    after_purchase_titles_string = get_macros_and_titles('AutomatedMacroTitles', 'Titles', 'Efter køb', 'title')
    before_purchase_titles_string = get_macros_and_titles('AutomatedMacroTitles', 'Titles', 'Før køb', 'title')
    club_matas_titles_string = get_macros_and_titles('AutomatedMacroTitles', 'Titles', 'Club Matas', 'title')
    other_titles_string = get_macros_and_titles('AutomatedMacroTitles', 'Titles', 'Andet', 'title')

    message_list = [{"role": "system", "content": f"""We have 12 different categories into which users' queries fall: After Purchase, Before Purchase, Other, Club Matas, Where is My Package, Can I Cancel My Order, Can I Change My Address, Wrong Item Received, Broken Product Received, Missing Item In My Order, Adding Items to an Order and Order Confirmation Not Received.

      Macro titles for After Purchase queries are:
      {after_purchase_titles_string}
    
      Macro titles for Before Purchase queries are:
      {before_purchase_titles_string}
    
      Macro titles for Other queries are:
      {other_titles_string}
    
      Macro titles for Club Matas queries are:
      {club_matas_titles_string}
    
      Macro titles for Where is My Package queries are:
      "Hvor er min pakke::Status::Tjek din pakkestatus"
      "Hvor er min pakke::Status::Find din pakkes placering"
      "Hvor er min pakke::Status::Find ud af, hvor din pakke er"
      "Hvor er min pakke::Status::Jeg kan ikke se nogen udvikling på sporingen"
      "Hvor er min pakke::Status::Sporingsinformation mangler"
      "Hvor er min pakke::Afhentning::Jeg har ikke modtaget meddelelse om, at min ordre er klar til afhentning"
      "Hvor er min pakke::Afhentning::Hvornår får jeg besked om, at min ordre er klar til afhentning?"
    
      Macro titles for Can I Cancel My Order queries are:
      "Kan jeg annullere min ordre::Annullering::Jeg vil ikke have min ordre, annuller den venligst"
      "Kan jeg annullere min ordre::Annullering::Kan jeg annullere min ordre"
      "Kan jeg annullere min ordre::Annullering::Min ordre er forsinket, jeg vil annullere den"
      "Kan jeg annullere min ordre::Annullering::Tjek annulleringsmuligheder"
    
      Macro titles for Can I Cancel My Order queries are:
      "Kan jeg ændre min adresse for den afgivne ordre::Adresseændring::Ordre leveret til min gamle adresse"
      "Kan jeg ændre min adresse for den afgivne ordre::Adresseændring::Ordre leveret til den forkerte butik"
      "Kan jeg ændre min adresse for den afgivne ordre::Adresseændring::Ordre leveret langt fra min adresse"
      "Kan jeg ændre min adresse for den afgivne ordre::Adresseændring::Tjek adresseændringsmuligheder"
    
      Macro titles for Wrong Item Received:
      "Forkert vare modtaget::Fejl i leveringen::Jeg har modtaget en forkert vare"
      "Forkert vare modtaget::Fejl i leveringen::Jeg bestilte noget andet, men modtog noget andet"
      "Forkert vare modtaget::Fejl i leveringen::Min ordre er forkert"
      "Forkert vare modtaget::Fejl i leveringen::Jeg modtog en vare, jeg ikke bestilte"
    
      Macro titles for Broken Product Received:
      "Modtaget beskadiget vare::Defekt produkt::Jeg har modtaget en beskadiget vare"
      "Modtaget beskadiget vare::Defekt produkt::Min vare er ødelagt"
      "Modtaget beskadiget vare::Defekt produkt::Produktet er beskadiget"
      "Modtaget beskadiget vare::Defekt produkt::Jeg har modtaget en defekt vare"
    
      Macro titles for Missing Item In My Order:
      "Manglende vare i ordre::Manglende produkt::En vare mangler i min ordre"
      "Manglende vare i ordre::Manglende produkt::Jeg har ikke modtaget alle varer i min ordre"
      "Manglende vare i ordre::Manglende produkt::Vare mangler i min levering"
      "Manglende vare i ordre::Manglende produkt::Der mangler noget i min pakke"
      "Manglende vare i ordre::Manglende produkt::Ordre delt i to dele - første del modtaget, anden del mangler"
      "Manglende vare i ordre::Manglende produkt::Bestilling opdelt - kun modtaget første del, anden del endnu ikke modtaget"
    
      Macro titles for Adding Items to an Order:
      "Kan jeg tilføje varer til min ordre::Tilføjelse af varer::Jeg vil gerne tilføje flere produkter til min eksisterende ordre"
      "Kan jeg tilføje varer til min ordre::Tilføjelse af varer::Kan jeg ændre min ordre for at inkludere flere varer?"
    
      Macro titles for Order Confirmation Not Received:
      "Ordrebekræftelse ikke modtaget::Bekræftelsesproblemer::Jeg har ikke modtaget en ordrebekræftelse"
      "Ordrebekræftelse ikke modtaget::Bekræftelsesproblemer::Kan du sende min ordrebekræftelse igen?"
    
      You will receive customer queries in Danish or English. Your task is to intelligently determine the category to which the user's query belongs using the above macro titles and by following the process outlined in the examples below and then activate the relevant function according to the determined Macro category from the user's query:
    
      Q: Hej, Jeg lagde mærke til, at Tanning Spray ikke var inkluderet i min seneste ordre. Hvad sker der, og hvordan kan dette løses?: Decision: Send ny ordre
      Category Determination: This particular query belongs to the 'After Purchase' category, as the customer is inquiring about missing items in the received order. Therefore, the function that should be activated is get_after_purchase_macros_response.
    
      Q: Hej, Jeg forsøgte at købe Paco Rabanne produktet, men det ser ud til at være udsolgt. Hvad kan jeg gøre for at få det, og ved du, hvornår det vil være tilgængeligt igen?: Decision: Tilmeld dig, så du får besked, når varen er på lager igen.
      Category Determination: This particular query belongs to the 'Before Purchase' category, as the customer is inquiring about the reavailability of a previously sold-out item. Therefore, the function that should be activated is get_before_purchase_macros_response.
    
      Q: Hej, Mit gavekort er netop udløbet for mindre end et år siden. Hvad kan jeg gøre, og er det muligt at få udstedt et nyt gavekort med samme værdi?: udstede nyt gavekort
      Category Determination: This particular query belongs to the 'Others' category, as the customer is inquiring about the process of renewing expired gift card. Therefore, the function that should be activated is get_other_macros_response.
    
      Q: Hej, Jeg har bemærket, at der er en anden e-mail på min profil. Kan du hjælpe mig med at ændre den? Hvad har du brug for af oplysninger for at bekræfte ændringen?: Decision: Vi skal bruge din fødselsdato og en ny e-mailadresse for at ændre din e-mail
      Category Determination: This particular query belongs to the 'Club Matas' category, as the customer is inquiring about the process of changing email profile. Therefore, the function that should be activated is get_club_matas_macros_response.
    
      Q: Hej, Hvad er status for min ordre med 22485519? Mvh, Camila
      Category Determination: This particular query belongs to the 'Where is My Package' category, as the customer is inquiring about the current status of their order. Therefore, the function that should be activated is get_where_is_my_package_response.
    
      Q: Hej, jeg har bestilt nogle varer til afhentning i butikken, men jeg har ikke modtaget nogen meddelelse om, at de er klar til afhentning endnu. Kan du hjælpe mig?
      Category Determination: This particular query belongs to the 'Where is My Package' category, specifically addressing the issue of not receiving a notification about the order being ready for pickup. Therefore, the function that should be activated is get_where_is_my_package_response.
    
      Q: Hej, Jeg håber det går godt. Jeg afgav en ordre for et par dage siden, men har ikke modtaget den. Kan du give mig en opdatering vedrørende det? Alina
      Category Determination: This particular query belongs to the 'Where is My Package' category, as the customer is requesting an update about the current status of their order. Therefore, the function that should be activated is get_where_is_my_package_response.
    
      Q: Kan jeg annullere min ordre med ordrenummer 23456987? Mvh, Albert
      Category Determination: This particular query belongs to the 'Can I Cancel My Order' category, as the customer is inquiring about the cancellation of their order. Therefore, the function that should be activated is get_can_i_cancel_my_order_response.
    
      Q: Hej, jeg kan se min pakke er blevet leveret på min gamle adresse, jeg har forsøgt at ændre det 3 gange nu, og de vare jeg har bestilt er til en gave i morgen, hvad kan jeg gøre? Jan jeg overhovedet få min pakke igen??
      Category Determination: This particular query belongs to the 'Can I Change My Address' category, as the customer is inquiring about changing the addrress of their order. Therefore, the function that should be activated is get_can_i_change_my_address_response.
    
      Q: Hej, jeg har modtaget en forkert vare i min ordre med ordrenummer 123456. Hvad skal jeg gøre nu?
      Category Determination: This query belongs to the 'Wrong Item Received' category, as the customer is reporting that they received an incorrect item. Therefore, the function that should be activated is wrong_item_has_been_received.
    
      Q: Hej, mit ordrenummer er 789012, og den vare, jeg har modtaget, er beskadiget. Hvad gør jeg nu?
      Category Determination: This query belongs to the 'Broken Product Received' category, as the customer is reporting that the received product is damaged. Therefore, the function that should be activated is broken_product_has_been_received.
    
      Q: Hej, jeg har ikke modtaget en af de varer, jeg bestilte med ordrenummer 345678. Kan du hjælpe mig?
      Category Determination: This query belongs to the 'Missing Item In My Order' category, as the customer is reporting that an item from their order is missing. Therefore, the function that should be activated is item_missing_in_order.
    
      Q: Hej, jeg placerede min ordre den 17. marts, og den blev delt i to. Jeg har modtaget den første del, men resten er endnu ikke kommet. Kan du hjælpe mig?
      Category Determination: This query belongs to the 'Missing Item In My Order' category, as the customer is reporting that a part of their order is missing. Therefore, the function that should be activated is item_missing_in_order.
      
      Q: Hej, Jeg har lige afgivet en ordre, men jeg vil gerne tilføje et par produkter mere. Er det muligt?
      Category Determination: This particular query belongs to the 'Adding Items to an Order' category, as the customer is inquiring about adding additional items to their existing order. Therefore, the function that should be activated is add_item_to_my_order_response.
    
      Q: Hej, Jeg har afgivet en ordre i går, men jeg har stadig ikke modtaget nogen ordrebekræftelse. Kan du hjælpe mig?
      Category Determination: This particular query belongs to the 'Order Confirmation Not Received' category, as the customer is inquiring about not receiving their order confirmation. Therefore, the function that should be activated is order_confirmation_not_received.
    
      Note: If the query is related to Wrong Item Received, Broken Product Received, Missing Item In My Order, Adding Items to an Order or Order Confirmation Not Received. do not activate get_after_purchase_macros_response; instead, activate the appropriate function: wrong_item_has_been_received, broken_product_has_been_received, item_missing_in_order, add_item_to_my_order_response or order_confirmation_not_received. If the query is related to not receiving the whole package, activate get_where_is_my_package_response instead of item_missing_in_order, as the latter is for specific products missing in the package.
      
      IMPORTANT: YOU MUST ALWAYS ACTIVATE A FUNCTION WITH REGARDS TO THE USER'S QUERY, EVEN FOR AMBIGUOUS AND WITHOUT CONTEXT QUERIES. ALSO, ALWAYS PASS THE FULL PROMPT TO THE FUNCTION AS INPUT. DO NOT REMOVE SENTENCES, SPECIALLY 'DECISION GIVEN' ON YOUR OWN.
      """}]
    
    logging.info("Choosing which function to call")
    new_message = {"role": "user", "content": prompt}
    message_list.append(new_message)
    response_message = openai_answers(message_list)
    response_message = response_message.to_dict()
    if response_message.get("function_call"):
        response_message['function_call'] = response_message['function_call'].to_dict()
        available_functions = {
            "get_after_purchase_macros_response": get_after_purchase_macros_response,
            "get_before_purchase_macros_response": get_before_purchase_macros_response,
            "get_other_macros_response": get_other_macros_response,
            "get_club_matas_macros_response": get_club_matas_macros_response,
            "get_where_is_my_package_response": get_where_is_my_package_response,
            "get_can_i_cancel_my_order_response": get_can_i_cancel_my_order_response,
            "get_can_i_change_my_address_response": get_can_i_change_my_address_response,
            "wrong_item_has_been_received": wrong_item_has_been_received,
            "broken_product_has_been_received": broken_product_has_been_received,
            "get_missing_item_or_missing_package": get_missing_item_or_missing_package,
            "add_item_to_my_order_response": add_item_to_my_order_response,
            "order_confirmation_not_received": order_confirmation_not_received

        }
        function_name = response_message["function_call"]["name"]

        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        if function_name in ("get_where_is_my_package_response", "get_can_i_cancel_my_order_response", "get_can_i_change_my_address_response", "add_item_to_my_order_response", "order_confirmation_not_received"):
            function_response = function_to_call(
                prompt=function_args.get("prompt"),
                user_email=user_email
            )
        elif function_name in ("wrong_item_has_been_received", "broken_product_has_been_received", "get_missing_item_or_missing_package"):
            function_response = function_to_call(
                prompt=function_args.get("prompt"),
                ticket_id = ticket_id,
                user_email=user_email
            )
        else:
            function_response = function_to_call(
                prompt=function_args.get("prompt")
            )

        response_message['content'] = None
        return function_response, function_name
        message_list = []

    else:
        return get_no_category_response(prompt), None

def get_claimlane_response(prompt, user_email, subject_check, ticket_id):
  logging.info('Getting Claimlane Response')
  if subject_check != 'Claimlane':
    claimlane_category = get_claimlane_category(prompt)
    if claimlane_category == 'Return':
      response = """Hej [Customer First Name],

      Super godt du skriver til os, når du ønsker at returnere din ordre.

      Vi vil meget gerne tage et kig på sagen.

      Jeg sender dig her et <a href="https://app.claimlane.com/c/matas?lang=da">link </a>, så du kan oprette en sag - så er vi sikre på at modtage alle de korrekte oplysninger for at kunne hjælpe dig bedst muligt. 

      Du hører fra os når vi har modtaget og behandlet din henvendelse.

      Sig endelig til hvis du har spørgsmål, eller hvis der er andet vi kan hjælpe med i mellemtiden. 

      Hav en dejlig dag."""

    elif claimlane_category == 'Claim/Defect':
      response = """Hej [Customer First Name],

      Super godt du skriver til os, når du ønsker at indberette en fejl eller mangel ved din ordre.

      Vi vil meget gerne tage et kig på sagen.

      Jeg sender dig her et <a href="https://app.claimlane.com/c/matas?lang=da">link </a>, så du kan oprette en sag - så er vi sikre på at modtage alle de korrekte oplysninger for at kunne hjælpe dig bedst muligt. 

      Du hører fra os når vi har modtaget og behandlet din henvendelse. 

      Sig endelig til hvis du har spørgsmål, eller hvis der er andet vi kan hjælpe med i mellemtiden. 

      Hav en dejlig dag."""

    elif claimlane_category == 'Missing Parts':
      response = """Hej [Customer First Name],

      Super godt du skriver til os, når du opdager at der mangler dele i din ordre.

      Vi vil meget gerne tage et kig på sagen.

      Jeg sender dig her et <a href="https://app.claimlane.com/c/matas?lang=da">link </a>, så du kan oprette en sag - så er vi sikre på at modtage alle de korrekte oplysninger for at kunne hjælpe dig bedst muligt. 

      Du hører fra os når vi har modtaget og behandlet din henvendelse.  

      Sig endelig til hvis du har spørgsmål, eller hvis der er andet vi kan hjælpe med i mellemtiden. 

      Hav en dejlig dag."""

    elif claimlane_category == 'Damaged in Transport':
      response = """Hej [Customer First Name],

      Super godt du skriver til os, når du opdager at din ordre er blevet beskadiget under transporten.

      Vi vil meget gerne tage et kig på sagen.

      Jeg sender dig her et <a href="https://app.claimlane.com/c/matas?lang=da">link </a>, så du kan oprette en sag - så er vi sikre på at modtage alle de korrekte oplysninger for at kunne hjælpe dig bedst muligt. 

      Du hører fra os når vi har modtaget og behandlet din henvendelse.  

      Sig endelig til hvis du har spørgsmål, eller hvis der er andet vi kan hjælpe med i mellemtiden. 

      Hav en dejlig dag."""

    elif claimlane_category == 'Lost/Incorrect Delivery':
      response = """Hej [Customer First Name],

      Super godt du skriver til os, når din ordre er blevet forlagt eller leveret forkert.

      Vi vil meget gerne tage et kig på sagen.

      Jeg sender dig her et <a href="https://app.claimlane.com/c/matas?lang=da">link </a>, så du kan oprette en sag - så er vi sikre på at modtage alle de korrekte oplysninger for at kunne hjælpe dig bedst muligt. 

      Du hører fra os når vi har modtaget og behandlet din henvendelse.

      Sig endelig til hvis du har spørgsmål, eller hvis der er andet vi kan hjælpe med i mellemtiden. 

      Hav en dejlig dag."""

    elif claimlane_category == 'Allergic Reaction':
      response = """Hej [Customer First Name],

      Det er super godt at du skriver. Jeg er meget ked af at høre den oplevelse du har haft med [Product Name]. 

      Jeg kan godt høre, at det tyder på, at du ikke kan tåle produktet. Det sker nogle gange, at der opstår en pludselig allergisk reaktion, og det kan også godt være, at det kun er den ene gang. Du kan få det testet hos en hudlæge/speciallæge og få konstateret, om der er en eller flere råvarer i produktet, du reagerer på. Du finder ingredienslisten på produktet, og ellers er du velkommen til at kontakte os for yderligere information. 

      Vi vil meget gerne tage hånd om din sag.

      Jeg sender dig her et <a href="https://app.claimlane.com/c/matas?lang=da">link </a>, så du kan oprette en sag - så er vi sikre på at modtage alle de korrekte oplysninger for at kunne hjælpe dig bedst muligt. 

      Du hører fra os når vi har modtaget og behandlet din henvendelse.  

      Sig endelig til hvis du har spørgsmål, eller hvis der er andet vi kan hjælpe med i mellemtiden. 

      Hav en dejlig dag."""

    else:
      response = """Hej [Customer First Name],

      Tak for din henvendelse! Vi sætter stor pris på, at du har taget dig tid til at kontakte os.

      Vi vil meget gerne tage et nærmere kig på din situation.

      Jeg sender dig her et <a href="https://app.claimlane.com/c/matas?lang=da">link </a>, så du kan oprette en sag - så er vi sikre på at modtage alle de korrekte oplysninger for at kunne hjælpe dig bedst muligt. 

      Du hører fra os når vi har modtaget og behandlet din henvendelse.

      Sig endelig til hvis du har spørgsmål, eller hvis der er andet vi kan hjælpe med i mellemtiden. 

      Hav en dejlig dag."""
    
    gpt_response = get_gpt_response(prompt, response, general=True, conditional=False, cancelled=False,
                                            tracking_history=None, logs=None)
    return gpt_response, None

  else:
    function_response, function_name = gpt_response_generator(prompt, user_email, ticket_id)
    return function_response, function_name



def identify_query_category(prompt, user_email, subject_check, ticket_id):
    logging.info('Identifying Query Category - Claimlane or General')
    message_list = [{"role": "system", "content": f"""We have 6 different claimlane categories: Return, Claim/Defect, Missing Parts, Damaged in Transport, Lost or Incorrect Delivery, and Allergic Reaction.

    You will receive customer queries in Danish or English. Your task is to intelligently determine if the query falls into any of these categories. If the query falls into any of the above categories, then the function that should be activated is get_claimlane_response. If it does not fall into any of these categories, activate gpt_response_generator.
    
    Q: Jeg har ikke modtaget denne pakke, trods den er bestilt for en uge siden. Varen SKAL bruges senest torsdag den 6/6, derfor haster det at lokalisere den, eller afsende en ny.
    The customer's query falls under the 'Lost/Incorrect Delivery' category of ClaimLane, as it concerns a package that has not been received. Therefore, the appropriate function to activate is: get_claimlane_response

    Q: Fortrydelsesret - returnering. Ønske om returlabel. Kære Matas Jeg har købt nogle suttehoveder pr. webordre som ikke passer mine sønner i størrelsen. Jeg ønsker derfor at returnere varen. Vil I være venlige at sende mig et returlabel til forsendelsen? Det drejer sig om ordrenummer: 18370962, hvor jeg ønsker at returnere 1 stk af : MAM Teat flaske sut Size 3. Mvh. Sandra Løfberg
    The customer's query falls under the 'Return' category of ClaimLane, as it concerns a request for returning the packahe. Therefore, the appropriate function to activate is: get_claimlane_response

    Q: Jeg har prøvet at opdatere min app fra Matas men kan ikke blive godkendt. Hvad er der galt jeg har været kunde i mange år. Mvh Merete Thorsen
    The customer's query does not fall into any of the 6 Claimlane categories, as it concerns an issue with update of Matas app. Therefore, the appropriate function to activate is: gpt_response_generator
                    
    Q: Hej Matas, Jeg ønsker at annullere ordren, hvis muligt. På forhånd tak
    The customer's query does not fall into any of the 6 Claimlane categories, as it concerns with the cancellation of an order. Therefore, the appropriate function to activate is: gpt_response_generator

    IMPORTANT: YOU MUST ALWAYS ACTIVATE A FUNCTION WITH REGARDS TO THE USER'S QUERY, EVEN FOR AMBIGUOUS AND WITHOUT CONTEXT QUERIES. ALSO, ALWAYS PASS THE FULL PROMPT TO THE FUNCTION AS INPUT. DO NOT REMOVE SENTENCES, SPECIALLY 'DECISION GIVEN' ON YOUR OWN."""}]
    
    new_message = {"role": "user", "content": prompt}
    message_list.append(new_message)
    response_message = openai_check_for_claimlane(message_list)
    response_message = response_message.to_dict()
    if response_message.get("function_call"):
        response_message['function_call'] = response_message['function_call'].to_dict()
        available_functions = {
            "get_claimlane_response": get_claimlane_response,
            "gpt_response_generator": gpt_response_generator
        }
        function_name_1 = response_message["function_call"]["name"]

        function_to_call = available_functions[function_name_1]
        function_args = json.loads(response_message["function_call"]["arguments"])
        if function_name_1 in ("get_claimlane_response"):
            function_response, function_name_2 = function_to_call(
                prompt=function_args.get("prompt"),
                user_email=user_email,
                subject_check = subject_check,
                ticket_id = ticket_id
            )
        else:
            function_response, function_name_2 = function_to_call(
                prompt=function_args.get("prompt"),
                user_email=user_email,
                ticket_id = ticket_id
            )
        response_message['content'] = None
        return function_response, function_name_2, function_name_1
        message_list = []

    else:
        return gpt_response_generator(prompt, user_email, ticket_id), None, None
