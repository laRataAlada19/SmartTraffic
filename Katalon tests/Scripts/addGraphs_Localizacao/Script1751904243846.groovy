import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.kms.katalon.core.testobject.TestObject as TestObject
import com.kms.katalon.core.testobject.ConditionType as ConditionType

// Abrir o browser e navegar
WebUI.openBrowser('')


WebUI.navigateToUrl('http://localhost:8001/')

// Click em "Login"
TestObject linkLogin = new TestObject()
linkLogin.addProperty("xpath", ConditionType.EQUALS, '//*[@id="app"]/div[2]/nav/a[5]')

WebUI.waitForElementVisible(linkLogin, 10)
WebUI.click(linkLogin)

//*[@id="app"]/div[2]/nav/button
//*[@id="app"]/div[2]/nav/a[5]
//*[@id="app"]/div[2]/nav/a[5]
// Inserir Email
WebUI.setText(customTestObject('xpath=//*[@id="email"]'), '1@gmail.com')

// Inserir Password
WebUI.setText(customTestObject('xpath=//*[@id="password"]'), '123')

// Click em botão "Login"
WebUI.click(customTestObject('xpath=//*[@id="app"]/div[2]/main/div/div[3]/button[2]'))

// Navegar para "Configuração"
WebUI.click(customTestObject('xpath=//*[@id="app"]/div[2]/nav/a[4]'))

// Selecionar opção (label 2)
WebUI.click(customTestObject('xpath=//*[@id="app"]/div[2]/main/div[2]/div/div[2]/div[1]/label[2]'))

// Confirmar seleção
WebUI.click(customTestObject('xpath=//*[@id="app"]/div[2]/main/button'))

// Ir para "Localizações"
WebUI.click(customTestObject('xpath=//*[@id="app"]/div[2]/nav/a[3]'))

// Click no botão da primeira linha da tabela (ícone)
WebUI.click(customTestObject('xpath=//*[@id="app"]/div[2]/main/div[1]/div/div/table/tbody/tr[1]/td[4]/button[1]/img'))

// Esperar que o gráfico apareça
WebUI.verifyElementVisible(customTestObject('xpath=//h3[contains(text(), "Distribuição de Veículos por Localização")]'))

// Fechar browser
WebUI.closeBrowser() // Função auxiliar para criar TestObjects dinamicamente

TestObject customTestObject(String xpath) {
    TestObject to = new TestObject()

    to.addProperty('xpath', ConditionType.EQUALS, xpath)

    return to
}

